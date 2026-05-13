"""
D10 Sample Artifact: Airflow DAG for Store POS CSV ingestion.

Design decisions:
- One task per store for fault isolation (one broken file doesn't block others)
- Per-store try/except: failed stores quarantined, not pipeline-halting
- Idempotency: GCS partition = source/pos/YYYY/MM/DD/store_id (overwrite)
- chardet detects encoding before parse
- Column normalization map handles header drift across register models
"""

from __future__ import annotations

import io
import logging
from datetime import datetime, timedelta

import chardet
import pandas as pd
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.sftp.hooks.sftp import SFTPHook

log = logging.getLogger(__name__)

# Canonical column names — maps known variants from older registers
COLUMN_NORMALIZATION_MAP = {
    "trans_date": "transaction_date",
    "transdate": "transaction_date",
    "sale_date": "transaction_date",
    "store_no": "store_id",
    "storeid": "store_id",
    "store_number": "store_id",
    "net_sales": "net_revenue_usd",
    "netsales": "net_revenue_usd",
    "revenue": "net_revenue_usd",
    "qty": "quantity",
    "quantity_sold": "quantity",
    "sku": "sku_id",
    "product_id": "sku_id",
    "item_code": "sku_id",
}

STORES = Variable.get("pos_store_list", deserialize_json=True)
GCS_BUCKET = Variable.get("bronze_gcs_bucket")
QUARANTINE_BUCKET = Variable.get("quarantine_gcs_bucket")
SFTP_CONN_ID = "pos_sftp"


def ingest_store_pos(store_id: str, execution_date: str, **context) -> None:
    sftp = SFTPHook(ssh_conn_id=SFTP_CONN_ID)
    gcs = GCSHook()

    remote_path = f"/exports/{store_id}/pos_{execution_date}.csv"
    date_path = execution_date.replace("-", "/")
    bronze_path = f"raw/pos/{date_path}/{store_id}/pos.parquet"
    quarantine_path = f"pos/{date_path}/{store_id}/pos_FAILED.csv"

    try:
        raw_bytes = sftp.retrieve_file_bytes(remote_path)

        # Detect encoding — older registers frequently send latin-1
        detected = chardet.detect(raw_bytes)
        encoding = detected.get("encoding", "utf-8") or "utf-8"
        log.info("Store %s: detected encoding %s (confidence %.2f)", store_id, encoding, detected.get("confidence", 0))

        df = pd.read_csv(io.BytesIO(raw_bytes), encoding=encoding, dtype=str)

        # Normalize column names
        df.columns = [COLUMN_NORMALIZATION_MAP.get(c.strip().lower(), c.strip().lower()) for c in df.columns]

        required_cols = {"transaction_date", "store_id", "sku_id", "net_revenue_usd", "quantity"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns after normalization: {missing}")

        df["store_id"] = store_id
        df["ingested_at"] = datetime.utcnow().isoformat()

        parquet_bytes = df.to_parquet(index=False)
        gcs.upload(
            bucket_name=GCS_BUCKET,
            object_name=bronze_path,
            data=parquet_bytes,
        )
        log.info("Store %s: %d rows written to gs://%s/%s", store_id, len(df), GCS_BUCKET, bronze_path)

    except Exception as exc:
        log.error("Store %s FAILED: %s — quarantining", store_id, exc)
        try:
            gcs.upload(
                bucket_name=QUARANTINE_BUCKET,
                object_name=quarantine_path,
                data=raw_bytes if "raw_bytes" in dir() else b"",
            )
        except Exception as q_exc:
            log.error("Store %s: quarantine upload also failed: %s", store_id, q_exc)

        # Do NOT re-raise — let other stores continue
        # PagerDuty alert is handled by a separate Airflow callback on task failure count
        context["ti"].xcom_push(key=f"failed_store_{store_id}", value=str(exc))


def alert_on_failures(**context) -> None:
    ti = context["ti"]
    failed = [k for k in ti.xcom_pull(task_ids=None, key=None) or [] if "failed_store" in str(k)]
    if failed:
        log.warning("POS ingestion completed with %d store failures: %s", len(failed), failed)
        # Hook into PagerDuty / Slack here via HTTP operator or webhook


with DAG(
    dag_id="pos_store_ingestion",
    description="Daily POS CSV ingestion from 160 stores via SFTP → GCS Bronze",
    schedule_interval="0 3 * * *",  # 03:00 UTC daily
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "owner": "data-engineering",
    },
    tags=["bronze", "pos", "batch", "finance"],
) as dag:

    store_tasks = [
        PythonOperator(
            task_id=f"ingest_store_{store_id}",
            python_callable=ingest_store_pos,
            op_kwargs={"store_id": store_id, "execution_date": "{{ ds }}"},
        )
        for store_id in STORES
    ]

    alert_task = PythonOperator(
        task_id="alert_on_failures",
        python_callable=alert_on_failures,
        trigger_rule="all_done",  # runs even if store tasks failed
    )

    store_tasks >> alert_task
