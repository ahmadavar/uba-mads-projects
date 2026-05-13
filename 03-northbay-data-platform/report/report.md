# NorthBay Pantry — Enterprise Data Platform Design
**DSCI 504 | Ahmad Var | May 13, 2026**

---

## D1 — Reference Architecture

NorthBay's platform follows the **Medallion Architecture** (Bronze → Silver → Gold) on Google Cloud, orchestrated by Apache Airflow for batch and Apache Kafka for streaming.

**Bronze (GCS):** Every source lands here raw and immutable — CSVs exactly as SFTP delivered them, Avro CDC events, WAV audio, scraped HTML. Nothing is transformed. This is the recovery layer: any downstream bug can be fixed by reprocessing from Bronze.

**Silver (BigQuery):** dbt models clean, validate, deduplicate, and standardize. Messy POS headers are normalized. Nested MongoDB JSON is flattened. Entity resolution produces a `golden_customer_master`. Bad rows are quarantined, not deleted.

**Gold (BigQuery):** Aggregated, role-gated business tables — `finance_daily_revenue`, `customer_360_view`, `marketing_attribution`. The feature store (Feast + Redis) serves ML models with sub-millisecond online lookup.

See `diagrams/architecture.mmd` for the full annotated diagram.

---

## D2 — Per-Source Ingestion Design

**Idempotency guarantee across all sources:** Bronze writes partition by `source/YYYY/MM/DD/run_id`. Re-runs overwrite the same partition path. Silver loads use `MERGE` (upsert) on a natural key — never blind `INSERT`. One failed re-run cannot double-count.

| # | Source | Tool | Cadence | Key Design Decisions |
|---|--------|------|---------|----------------------|
| 1 | NorthBay OLTP (PostgreSQL) | Debezium → Kafka → Kafka Connect | Real-time | CDC captures every INSERT/UPDATE/DELETE. MERGE on primary key in Silver. |
| 2 | Product Catalog (MongoDB) | MongoDB Change Streams → Kafka | Real-time | `_id + updatedAt` as dedup key. Nested attrs flattened in Silver dbt model. |
| 3 | Salesforce | Airflow HttpSensor + paginated REST + webhook | Every 4 hrs + real-time webhook | Exponential backoff on 429. Checkpoint `cursor_id` to resume pagination. Upsert on `case_id`. |
| 4 | Store POS (CSV/SFTP) | Airflow SFTPOperator — one task per store | Daily 03:00 UTC | Per-store fault isolation: one broken file → quarantine bucket + alert. `chardet` detects encoding. Column-name normalization map in Silver. |
| 5 | Mobile App Events | Flink/Spark Streaming consuming Kafka | Continuous | Schema Registry enforces Avro contract. Schema mismatch → dead-letter topic. Kafka offset commit after Bronze write. |
| 6 | PantryPlus Loyalty | Airflow + token-bucket rate limiter | Daily + webhook | 60 req/min enforced in operator. Upsert on `member_id + snapshot_date`. |
| 7 | Customer Reviews | Airflow + Scrapy | Daily batch | Respects `robots.txt`. `hash(review_site + review_id)` as dedup key. `langdetect` tags language. |
| 8 | Marketing Platforms (4x) | Airflow — one DAG per platform | Daily + hourly | Platform-level fault isolation. Unified spend schema applied in Silver. Upsert on `platform + campaign_id + date`. |
| 9 | Supplier EDI/XML | Airflow FTPOperator | Daily | `lxml` parses XML. Malformed files → quarantine + supplier email alert. Per-supplier schema map. `filename + invoice_id` dedup key. |
| 10 | Support Calls (WAV) | S3 event → SQS → Lambda → Airflow + AWS Transcribe | Continuous | Encrypted at rest (SSE-S3). PII flagged. Transcript stored with call `UUID`. Failed transcriptions → retry queue. |

---

## D3 — Storage Architecture

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Bronze | GCS / S3 | Cheapest $/GB; no schema required; handles binary (WAV, HTML) |
| Silver / Gold | BigQuery | Columnar → sub-second aggregations; dbt-native; TB-scale joins |
| Streaming buffer | Apache Kafka | Decouples producers from consumers; replay; Schema Registry |
| Feature store (online) | Feast + Redis | Redis serves features in <5ms — needed for 2-sec Customer Success SLA |
| Feature store (offline) | Feast + BigQuery | Training data for churn, forecast, recommender models |
| Audio + large binary | S3 | Object storage is the only viable option for WAV blobs |

**Why not a single system:** BigQuery cannot store WAV files. S3 cannot answer `SELECT SUM(revenue) GROUP BY store` in milliseconds. Redis exists because BigQuery's query latency (~1–3 sec) violates the Customer Success 2-second SLA.

---

## D4 — Curation and Standardization Plan

### Entity Resolution — "Customer"

The customer entity is fragmented across 6 sources: OLTP (email), Salesforce (phone + email), PantryPlus (loyalty ID + email variant), Mobile App (device ID), Marketing platforms (hashed email), Reviews (username). No single identifier is universal.

**Resolution approach (probabilistic matching):**

1. **Deterministic pass:** Exact match on normalized email (`lower() + strip()`). If matched → same customer.
2. **Probabilistic pass (Splink / DuckDB):** Score pairs on (normalized name, phone Soundex, address zip). Threshold ≥ 0.85 → merge candidate.
3. **Golden record:** One `customer_uuid` (UUID v4, generated at first resolution) written to `golden_customer_master`. All source tables carry a `customer_uuid` FK in Silver.
4. **Survivorship rule:** Most recently updated non-null field wins. Email from OLTP is canonical if present.

### Master Data — "Product"

MongoDB is the system of record for SKUs. Silver `golden_product_master` flattens nested attributes, standardizes allergen codes (FALCPA standard), and maps supplier hierarchy. `sku_id` from OLTP is the canonical key.

### Standardization Rules (applied in Silver dbt models)

| Dimension | Rule |
|-----------|------|
| Currency | All amounts converted to USD at daily ECB rate; original currency stored |
| Time zone | All timestamps stored as UTC; display TZ applied at query layer |
| Country codes | ISO 3166-1 alpha-2 |
| Units | Metric (kg, ml) canonical; imperial stored as-is for US display |
| Phone | E.164 format after normalization |
| Email | `lower().strip()` |

---

## D5 — Data Quality Framework

| Check | Layer | Tool | Owner | Bad Data Action |
|-------|-------|------|-------|-----------------|
| Schema conformance | Bronze ingest | Great Expectations | Data Engineering | Quarantine file; alert Slack #data-alerts |
| Null rate on required fields | Silver dbt | dbt tests (`not_null`) | Data Steward | Block Silver load; PagerDuty P2 |
| Referential integrity (FK) | Silver dbt | dbt tests (`relationships`) | Data Steward | Log violation; do not block |
| Row count vs. prior day ±20% | Silver dbt | dbt tests + custom | Data Engineering | PagerDuty P1 if Finance table |
| Duplicate primary keys | Silver dbt | dbt tests (`unique`) | Data Engineering | Block load; alert |
| PII present in non-PII table | Gold | GE custom expectation | Privacy team | Block + incident ticket |
| Finance table immutability | Gold | Row-level audit trigger | Finance owner | Block + SOX violation alert |
| Freshness SLA | Gold | Airflow SLA miss callback | Data Engineering | PagerDuty P1 if 7AM miss |

Results surfaced in a **DataHub** data quality dashboard. Quarantined rows land in `bq_quarantine` dataset with reason code and timestamp. Never deleted — reviewed weekly by data stewards.

---

## D6 — Metadata and Data Catalog

**Tool: DataHub (open-source)**

| Metadata Type | Captured How |
|---------------|-------------|
| Schema / column lineage | Automatically via Airflow + dbt integration |
| PII column tags | dbt `meta: {pii: true}` propagated to DataHub |
| Data owner + steward | Manually tagged at dataset creation; required field |
| Freshness / row counts | Airflow emits stats to DataHub on each DAG run |
| Business glossary | Manually maintained (Finance owns "revenue" definition) |
| Source-to-Gold lineage | dbt `--select +model+` lineage auto-ingested |

**Tagging model:** Every dataset tagged with: `domain` (Finance/Marketing/etc.), `sensitivity` (public/internal/confidential/restricted), `pii` (boolean), `source_system`, `owner`.

---

## D7 — Governance Model

**Roles:**
- **Data Owner:** Business unit VP. Accountable for accuracy and access policy.
- **Data Steward:** Embedded analyst. Reviews quarantine queue, approves schema changes.
- **Data Custodian:** Data Engineering. Implements access controls, runs pipelines.

**RACI for Top 5 Datasets:**

| Dataset | Data Owner | Data Steward | Data Custodian | Legal/Privacy |
|---------|------------|--------------|----------------|---------------|
| `golden_customer_master` | VP Customer Success | CS Analyst | Data Eng | Consulted |
| `finance_daily_revenue` | CFO | Finance Analyst | Data Eng | Informed |
| `stg_call_transcripts` | VP Customer Success | CS Analyst | Data Eng | Accountable |
| `marketing_attribution` | CMO | Marketing Analyst | Data Eng | Informed |
| `golden_product_master` | VP Merchandising | Merch Analyst | Data Eng | Informed |

---

## D8 — Security and Compliance Plan

### PII Inventory

| Source | PII Fields | Sensitivity |
|--------|-----------|-------------|
| OLTP | name, email, address, order history | Confidential |
| Salesforce | name, email, phone, case notes | Confidential |
| Loyalty | name, email, phone, tier, points | Confidential |
| Support Calls | voice recording, transcript | **Restricted** |
| Reviews | username (pseudonymous) | Internal |

### Controls

- **Encryption at rest:** AES-256 on all GCS buckets and BigQuery datasets. WAV files use SSE-S3 with customer-managed keys (CMEK).
- **Encryption in transit:** TLS 1.3 for all API calls, Kafka, and BigQuery connections.
- **Access control:** BigQuery column-level security. Transcripts accessible only to `role:customer_success`. PII columns masked for all other roles via BigQuery policy tags.
- **Audit logging:** Cloud Audit Logs captures every BigQuery query, GCS access, and IAM change. Retained 7 years (SOX requirement).
- **SOX tables:** `finance_daily_revenue` and related tables are append-only. No UPDATE/DELETE permitted. Change-controlled via dbt PR approval process.

### GDPR Right-to-Erasure Runbook

**Trigger:** Privacy team receives erasure request for customer X.

**Steps (must complete within 30 days; target: 5 business days):**

1. Look up `customer_uuid` in `golden_customer_master` using email/phone.
2. Query DataHub lineage to list every table containing `customer_uuid` FK — automated via DataHub API.
3. Run erasure dbt macro: nullifies PII columns in Silver (`golden_customer_master`, `stg_customers`, `stg_cases`, `stg_loyalty_members`). Replaces with `[ERASED-{date}]`.
4. Delete WAV files from S3 using call `UUID` index. Delete associated transcripts from BigQuery.
5. Submit deletion request to third-party systems: Salesforce API, PantryPlus SaaS vendor.
6. Bronze layer: PII is not deleted (immutable raw) — this is permissible under GDPR "legitimate interests for audit" exception, documented in Records of Processing Activities (RoPA). Data is encrypted and access-restricted.
7. Log erasure completion in `gdpr_erasure_log` table (audit trail).
8. Notify customer within 30-day SLA.

---

## D9 — Monitoring and Operations

### Pipeline SLAs

| Pipeline | SLA | P-level if missed |
|----------|-----|-------------------|
| Finance daily revenue | Available by 07:00 ET | P1 — page on-call immediately |
| Store POS ingestion | Complete by 05:00 ET | P1 — Finance SLA depends on it |
| Customer 360 lookup | <2 sec response | P2 — page within 15 min |
| Silver refresh | Complete by 06:00 ET | P1 |
| Loyalty / Marketing | Complete by 09:00 ET | P2 |

### Key Metrics (Airflow + Datadog)

- DAG success rate per source
- Bronze → Silver lag (minutes)
- Quarantine rate per source (% rows rejected)
- Kafka consumer lag (events/sec behind)
- BigQuery slot utilization + cost per DAG
- Data freshness per Gold table

### Alerting Flow

```
Airflow SLA miss callback
        ↓
PagerDuty (severity by table)
        ↓
On-call Data Engineer (15 min response P1 / 1 hr P2)
        ↓
Slack #data-incidents auto-post with DAG link + last success timestamp
```

**On-call:** Weekly rotation among 3 data engineers. Runbooks stored in Confluence. Each DAG has a `runbook_url` tag in Airflow.

### Cost Tagging

Every BigQuery job and GCS operation tagged with: `team`, `source_system`, `environment`, `dag_id`. Monthly cost reports by domain surfaced to each VP.

---

## D10 — Sample Artifacts

See `artifacts/` directory for:
- `dags/pos_ingestion_dag.py` — Airflow DAG for Store POS ingestion
- `dbt/stg_pos_transactions.sql` — dbt Silver staging model
- `great_expectations/pos_suite.py` — Great Expectations validation suite
- `dags/alert_callback.py` — SLA miss alert callback

---

## D11 — Cost and Risk Discussion

### Rough Monthly Run Cost

| Component | Estimated Monthly Cost |
|-----------|----------------------|
| BigQuery (storage + queries) | ~$4,000–$8,000 |
| GCS / S3 (Bronze + audio) | ~$2,000–$3,500 |
| Kafka (Confluent Cloud or self-hosted) | ~$3,000–$5,000 |
| Airflow (Cloud Composer or MWAA) | ~$2,000–$3,000 |
| AWS Transcribe (250 hrs/day audio) | ~$8,000–$12,000 |
| DataHub (self-hosted on GKE) | ~$500–$1,000 |
| Redis (Feast online store) | ~$500–$1,000 |
| **Total** | **~$20,000–$33,500/month** |

*Audio transcription is the dominant cost driver. Evaluate selective transcription (only escalated calls) to reduce by ~60%.*

### Top 3 Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **POS schema drift breaks Silver** | High (column drift is documented) | High (Finance SLA missed) | Schema evolution tests in CI; dbt `accepted_values` on critical columns; quarantine-and-alert on unknown columns |
| **Kafka consumer lag during mobile event spike** | Medium | Medium (stale clickstream data) | Auto-scaling consumer group; Kafka topic retention set to 7 days to allow replay; lag alert at 100K events behind |
| **GDPR erasure misses a table** | Low | Critical (regulatory fine up to 4% global revenue) | DataHub lineage makes all `customer_uuid` FK tables discoverable; erasure macro tested quarterly with synthetic customer; erasure log audited by Legal monthly |

---

## Concrete Questions Answered

1. **How does data flow from each source into the platform?** See D2 ingestion table and `architecture.mmd`.
2. **Where does each dataset live and why?** See D3 storage architecture table.
3. **How do you guarantee re-running a pipeline does not double-count?** Bronze partitioned by `source/date/run_id` (overwrite semantics). Silver uses MERGE on natural key.
4. **How do you uniquely identify a single customer across all 10 sources?** Deterministic email match + probabilistic Splink scoring → single `customer_uuid` in `golden_customer_master`.
5. **How would you find every row of data about customer X in under one hour for GDPR erasure?** DataHub lineage API lists every table with `customer_uuid` FK in seconds. Erasure macro runs in minutes.
6. **Which datasets are most sensitive, and how is access controlled?** Support call transcripts (Restricted) and customer PII (Confidential). BigQuery column-level policy tags + IAM roles enforce access. Only `role:customer_success` can read transcripts.
7. **If the Finance dashboard is missing at 7:00 AM, what process detects and resolves it?** Airflow SLA miss callback fires at 07:00 ET → PagerDuty P1 → on-call engineer paged → Slack #data-incidents auto-posted with last successful run timestamp and runbook link.
