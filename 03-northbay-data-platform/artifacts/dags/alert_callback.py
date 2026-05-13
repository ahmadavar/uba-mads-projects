"""
D10 Sample Artifact: Airflow SLA miss callback for Finance dashboard pipeline.

Fires when any task in the finance_gold_refresh DAG misses its SLA.
Sends PagerDuty P1 + Slack #data-incidents with context for on-call engineer.
"""

import json
import logging
from datetime import datetime

import requests
from airflow.models import Variable

log = logging.getLogger(__name__)

PAGERDUTY_ROUTING_KEY = Variable.get("pagerduty_routing_key_p1")
SLACK_WEBHOOK = Variable.get("slack_data_incidents_webhook")
RUNBOOK_URL = "https://confluence.northbaypantry.com/wiki/finance-dashboard-runbook"


def finance_sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """
    Called by Airflow when SLA is missed on finance_gold_refresh DAG.
    Fires at 07:00 ET if pipeline hasn't completed.
    """
    missed_tasks = [sla.task_id for sla in slas]
    blocking_tasks = [ti.task_id for ti in blocking_tis]

    log.error(
        "SLA MISS — finance_gold_refresh | missed: %s | blocking: %s",
        missed_tasks,
        blocking_tasks,
    )

    _page_pagerduty(missed_tasks, blocking_tasks, dag.dag_id)
    _alert_slack(missed_tasks, blocking_tasks, dag.dag_id)


def _page_pagerduty(missed_tasks: list, blocking_tasks: list, dag_id: str) -> None:
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "payload": {
            "summary": f"P1: Finance dashboard SLA missed — {dag_id}",
            "severity": "critical",
            "source": "airflow",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "custom_details": {
                "dag_id": dag_id,
                "missed_tasks": missed_tasks,
                "blocking_tasks": blocking_tasks,
                "runbook": RUNBOOK_URL,
                "sla": "Finance dashboard must be available by 07:00 ET",
            },
        },
        "links": [{"href": RUNBOOK_URL, "text": "On-call Runbook"}],
    }
    try:
        resp = requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        resp.raise_for_status()
        log.info("PagerDuty P1 triggered: %s", resp.json().get("dedup_key"))
    except Exception as exc:
        log.error("PagerDuty call failed: %s", exc)


def _alert_slack(missed_tasks: list, blocking_tasks: list, dag_id: str) -> None:
    message = {
        "text": (
            f":red_circle: *P1 — Finance Dashboard SLA Missed*\n"
            f"*DAG:* `{dag_id}`\n"
            f"*Missed tasks:* `{', '.join(missed_tasks)}`\n"
            f"*Blocking:* `{', '.join(blocking_tasks)}`\n"
            f"*SLA:* Finance dashboard available by 07:00 ET\n"
            f"*Action:* <{RUNBOOK_URL}|Open runbook> — check last successful run in Airflow UI"
        )
    }
    try:
        resp = requests.post(SLACK_WEBHOOK, json=message, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        log.error("Slack alert failed: %s", exc)
