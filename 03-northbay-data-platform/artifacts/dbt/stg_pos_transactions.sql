-- D10 Sample Artifact: dbt Silver staging model for Store POS transactions.
--
-- Design decisions:
-- - Reads from Bronze external table (GCS Parquet) via BigQuery external table
-- - Casts all fields explicitly — Bronze is all strings (safe from CSV parsing)
-- - Deduplicates on (store_id, transaction_date, sku_id, register_id) using row_number
--   Idempotency: re-running this model produces the same output (incremental merge on pk)
-- - PII note: no customer PII in POS — only store/SKU/revenue data
-- - SOX note: net_revenue_usd is a SOX-controlled field; no updates after load

{{ config(
    materialized='incremental',
    unique_key='pos_transaction_id',
    incremental_strategy='merge',
    on_schema_change='fail',
    tags=['silver', 'finance', 'pos', 'sox']
) }}

with raw_pos as (
    select
        store_id,
        sku_id,
        -- Cast from string; SAFE_CAST returns NULL instead of erroring on bad values
        safe_cast(transaction_date as date)            as transaction_date,
        safe_cast(net_revenue_usd as numeric)          as net_revenue_usd,
        safe_cast(quantity as int64)                   as quantity,
        coalesce(register_id, 'UNKNOWN')               as register_id,
        ingested_at,
        -- Dedup ranking: keep the row with latest ingested_at per natural key
        row_number() over (
            partition by store_id, transaction_date, sku_id, register_id
            order by ingested_at desc
        ) as row_rank
    from {{ source('bronze', 'pos_raw') }}
    {% if is_incremental() %}
    -- Only process partitions newer than the last load
    where date(ingested_at) >= (
        select date_sub(max(date(ingested_at)), interval 1 day)
        from {{ this }}
    )
    {% endif %}
),

deduped as (
    select * from raw_pos where row_rank = 1
),

validated as (
    select
        -- Surrogate key: deterministic hash of natural key
        {{ dbt_utils.generate_surrogate_key([
            'store_id', 'transaction_date', 'sku_id', 'register_id'
        ]) }}                                          as pos_transaction_id,
        store_id,
        sku_id,
        transaction_date,
        net_revenue_usd,
        quantity,
        register_id,
        ingested_at,
        -- Data quality flags (rows are NOT dropped — quarantine logic in tests)
        transaction_date is null                       as dq_missing_date,
        net_revenue_usd is null                        as dq_missing_revenue,
        net_revenue_usd < 0                            as dq_negative_revenue,
        quantity is null or quantity <= 0              as dq_invalid_quantity
    from deduped
    where
        -- Hard filter: rows with no date or store are unresolvable
        transaction_date is not null
        and store_id is not null
        and sku_id is not null
)

select * from validated
