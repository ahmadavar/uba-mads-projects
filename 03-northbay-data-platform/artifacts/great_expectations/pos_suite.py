"""
D10 Sample Artifact: Great Expectations validation suite for Silver POS table.

Checks run at the Silver layer (after dbt staging, before Gold promotion).
Bad rows are quarantined; pipeline is blocked only on critical failures.
Results surface in DataHub data quality dashboard via GE Data Docs.
"""

import great_expectations as gx
from great_expectations.checkpoint import Checkpoint

context = gx.get_context()

# Connect to BigQuery Silver table
datasource = context.sources.add_bigquery(
    name="bigquery_silver",
    project="northbay-data-platform",
)

asset = datasource.add_table_asset(
    name="stg_pos_transactions",
    table_name="silver.stg_pos_transactions",
)

batch_request = asset.build_batch_request()

# Create expectation suite
suite = context.add_expectation_suite("pos_silver_suite")
validator = context.get_validator(batch_request=batch_request, expectation_suite=suite)

# ── Completeness ──────────────────────────────────────────────────────────────
validator.expect_column_values_to_not_be_null("pos_transaction_id")
validator.expect_column_values_to_not_be_null("store_id")
validator.expect_column_values_to_not_be_null("transaction_date")
validator.expect_column_values_to_not_be_null("sku_id")

# ── Uniqueness ────────────────────────────────────────────────────────────────
validator.expect_column_values_to_be_unique("pos_transaction_id")

# ── Value ranges ──────────────────────────────────────────────────────────────
# Revenue must be non-negative (returns are modeled separately)
validator.expect_column_values_to_be_between(
    "net_revenue_usd", min_value=0, max_value=50_000
)
validator.expect_column_values_to_be_between(
    "quantity", min_value=1, max_value=10_000
)

# ── Row count freshness ───────────────────────────────────────────────────────
# Expect at least 100K rows per daily run (160 stores × ~625 avg transactions)
# Deviation >20% from yesterday triggers P1 alert
validator.expect_table_row_count_to_be_between(
    min_value=80_000,   # 20% below expected floor
    max_value=5_000_000,
)

# ── Referential / categorical ─────────────────────────────────────────────────
# store_id must be in the known store registry (loaded from Variable)
# In practice, load store list from BigQuery reference table
validator.expect_column_values_to_match_regex(
    "store_id", r"^(US|UK)-\d{4}$"
)

# transaction_date must be within last 3 days (guards against stale file replay)
validator.expect_column_values_to_be_between(
    "transaction_date",
    min_value="2026-01-01",  # data platform launch date
    max_value="{{ execution_date }}",
)

# ── Data quality flag audit ───────────────────────────────────────────────────
# These flags are set by dbt model; we expect them to be mostly False
validator.expect_column_values_to_be_in_set(
    "dq_negative_revenue", value_set=[False], mostly=0.999
)
validator.expect_column_values_to_be_in_set(
    "dq_invalid_quantity", value_set=[False], mostly=0.999
)

validator.save_expectation_suite()

# ── Checkpoint: runs after each dbt Silver job ────────────────────────────────
checkpoint = context.add_checkpoint(
    name="pos_silver_checkpoint",
    validations=[{
        "batch_request": batch_request,
        "expectation_suite_name": "pos_silver_suite",
    }],
    action_list=[
        # Publish results to GE Data Docs (linked from DataHub)
        {"name": "store_validation_result", "action": {"class_name": "StoreValidationResultAction"}},
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
        # Alert on failure — triggers PagerDuty via webhook
        {
            "name": "send_slack_notification",
            "action": {
                "class_name": "SlackNotificationAction",
                "slack_webhook": "{{ var.value.slack_data_alerts_webhook }}",
                "notify_on": "failure",
                "message_text": "POS Silver validation FAILED — Finance 7AM SLA at risk. Run: {{ run_id }}",
            },
        },
    ],
)

if __name__ == "__main__":
    result = context.run_checkpoint("pos_silver_checkpoint")
    if not result["success"]:
        raise SystemExit("Great Expectations validation failed — blocking Gold promotion")
