# D12 — Presentation Outline
## NorthBay Pantry Enterprise Data Platform
**DSCI 504 | Ahmad Var | 15–20 minutes**

---

## Slide Structure (16 slides)

---

### Slide 1 — Title
**NorthBay Pantry: Building an Enterprise Data Platform from Scratch**
- Ahmad Var | DSCI 504 | UBA MADS

---

### Slide 2 — The Problem (set the stage)
**NorthBay has $1.4B in revenue and zero data infrastructure**

- 160 stores across US + UK
- E-commerce + meal-kit subscription (Pantry Box) + loyalty program (PantryPlus)
- **10 data sources**: some streaming at 80K events/min, some nightly CSV files with garbled headers, some audio files
- Finance can't see revenue until manually assembled. Customer Success doesn't know a caller's order history. Data Science can't train models.
- *This is a greenfield build.*

> Speaker note: Frame the stakes. Without this platform, the company is flying blind at $1.4B scale.

---

### Slide 3 — Design Philosophy
**One guiding principle: match tool to workload**

- A single database cannot serve real-time event streaming, sub-second dashboards, and 5-year model training simultaneously
- Three questions drove every decision:
  1. What is the shape of the data? (structured / semi-structured / binary)
  2. What is the access pattern? (streaming / batch / sub-second lookup)
  3. Who owns the data and who can see it?

> Speaker note: This slide is your credibility anchor. Engineering decisions are principled, not arbitrary.

---

### Slide 4 — D1: Reference Architecture
**The Medallion Architecture: Bronze → Silver → Gold**

```
10 Sources → Ingestion Layer → Bronze (GCS) → Silver (BigQuery) → Gold (BigQuery) → Consumers
                                   ↑                  ↑                  ↑
                               Raw, immutable     Cleaned, validated   Business-ready
                               never modified     bad rows quarantined  role-gated
```

- **Bronze (GCS):** Raw files, forever. The recovery layer — any bug downstream can be fixed by reprocessing from here.
- **Silver (BigQuery):** dbt cleans, validates, deduplicates. Entity resolution produces one `customer_uuid` per person.
- **Gold (BigQuery):** What Finance, Marketing, and Data Science actually query. Access enforced by role.
- **Feature Store (Feast + Redis):** ML features served in <5ms for the Customer Success 2-second SLA.

> Speaker note: Show architecture.mmd diagram here. Walk left to right.

---

### Slide 5 — D2: Ingestion — 10 Sources, 3 Patterns
**Not all sources are equal**

| Pattern | Sources | Tool |
|---------|---------|------|
| Streaming (real-time) | OLTP CDC, Mobile Events, MongoDB | Debezium → Kafka → Kafka Connect |
| Batch (scheduled) | POS CSV, Salesforce, Loyalty, Marketing, Supplier EDI | Apache Airflow |
| Event-driven (continuous) | Support Call WAV files | S3 → SQS → Lambda → AWS Transcribe |

**Key design decisions:**
- **Fault isolation on POS:** One task per store. One broken CSV → quarantine bucket + alert. 159 other stores continue.
- **Idempotency everywhere:** Bronze partitioned by `source/YYYY/MM/DD/run_id`. Re-runs overwrite same partition — no double-counting.
- **Rate limiting:** PantryPlus API capped at 60 req/min via token-bucket limiter in Airflow operator.

> Speaker note: The POS fault isolation story is concrete and memorable. Use it.

---

### Slide 6 — D3: Storage Architecture
**Right tool for the right workload**

| What | Where | Why |
|------|-------|-----|
| Raw files, WAV audio, HTML | GCS / S3 | Cheapest $/GB; no schema; handles binary |
| Cleaned tables + dashboards | BigQuery | Columnar, TB-scale, sub-second aggregations |
| In-flight events | Kafka | Decouples producers from consumers; replay |
| ML online features | Feast + Redis | <5ms lookup — BigQuery's 1–3 sec violates 2-sec SLA |

> Speaker note: "Why not one system?" BigQuery can't store WAV. S3 can't answer SUM(revenue) in milliseconds. Redis exists for one specific SLA violation.

---

### Slide 7 — D4: Curation — The Customer Identity Problem
**Same person, 6 different records**

- "ahmad.var@gmail.com" in OLTP
- "AHMAD VAR" + phone in Salesforce
- "ahmadvar@gmail.com" in PantryPlus loyalty
- Device ID in Mobile App

**Entity resolution pipeline:**
1. Deterministic pass: exact match on normalized email (`lower().strip()`)
2. Probabilistic pass (Splink): score on name + phone Soundex + zip. Threshold ≥ 0.85 → merge
3. Outcome: one `customer_uuid` (UUID v4) written to `golden_customer_master`
4. Survivorship rule: most recently updated non-null field wins

**Also:** `golden_product_master` standardizes allergen codes (FALCPA), supplier hierarchy, and flattens nested MongoDB attrs. All amounts → USD. All timestamps → UTC.

> Speaker note: The "same person, 6 records" framing is sticky — use the concrete name example.

---

### Slide 8 — D5: Data Quality Framework
**Bad data has a home — but it's not Production**

| Check | Layer | If it fails |
|-------|-------|-------------|
| Schema conformance | Bronze (Great Expectations) | Quarantine file, Slack alert |
| Null rate on required fields | Silver (dbt `not_null`) | Block Silver load, PagerDuty P2 |
| Duplicate primary keys | Silver (dbt `unique`) | Block load, alert |
| Row count ±20% vs. prior day | Silver | PagerDuty P1 if Finance table |
| PII in non-PII table | Gold | Block + incident ticket |
| Finance table immutability | Gold | Block + SOX violation alert |

- Quarantined rows land in `bq_quarantine` with reason code + timestamp. Never deleted.
- Results surfaced in **DataHub** data quality dashboard.

> Speaker note: "Bad rows have an address, not a death sentence." They're in quarantine, reviewable, reprocessable.

---

### Slide 9 — D6 + D7: Catalog and Governance
**Who owns what, and where to find it**

**DataHub (open-source catalog):**
- Every column tagged: `domain`, `sensitivity`, `pii`, `source_system`, `owner`
- Source-to-Gold lineage auto-ingested from dbt
- PII column tags flow from dbt `meta: {pii: true}` → DataHub → access control enforcement

**Governance — 3 roles, clear accountability:**
- **Data Owner (VP):** Accountable for accuracy and access policy
- **Data Steward (Analyst):** Reviews quarantine queue, approves schema changes
- **Data Custodian (Data Eng):** Implements controls, runs pipelines

**RACI highlight:** `stg_call_transcripts` — Legal/Privacy is *Accountable* (not just Informed). Voice recordings require the highest accountability level.

---

### Slide 10 — D8: Security and Compliance
**Two regulatory frameworks, one platform**

**Access controls:**
- BigQuery column-level policy tags: call transcripts accessible only to `role:customer_success`
- AES-256 at rest on all GCS/BigQuery. WAV files use CMEK. TLS 1.3 in transit.
- Cloud Audit Logs retained 7 years (SOX requirement)

**GDPR Right-to-Erasure — 5-day runbook:**
1. Look up `customer_uuid` in `golden_customer_master`
2. DataHub lineage API lists every table with `customer_uuid` FK — in seconds
3. Erasure dbt macro: nullify PII columns in Silver → `[ERASED-{date}]`
4. Delete WAV + transcripts by call UUID
5. Submit deletion to Salesforce + PantryPlus SaaS APIs
6. Log in `gdpr_erasure_log` (audit trail)

> Speaker note: The DataHub lineage answer to "find every row about customer X" is the sharpest concrete answer in the project. Lean into it.

---

### Slide 11 — D9: Monitoring and Operations
**The Finance team can't wait. Neither can the on-call engineer.**

**SLAs:**
| Pipeline | SLA | Alert level |
|----------|-----|-------------|
| Finance daily revenue | 07:00 ET | P1 — page immediately |
| Store POS ingestion | 05:00 ET | P1 |
| Customer 360 lookup | <2 sec | P2 — 15 min |

**Alerting chain:**
```
Airflow SLA miss → PagerDuty (P1/P2) → On-call engineer → Slack #data-incidents
```
- On-call: weekly rotation among 3 engineers
- Each DAG has a `runbook_url` tag — engineer lands on the runbook in one click
- Cost tagging on every BigQuery job: monthly reports by domain surfaced to each VP

---

### Slide 12 — D10: Sample Artifacts
**The design is backed by working code**

Four artifacts in `artifacts/`:

| File | What it demonstrates |
|------|---------------------|
| `dags/pos_ingestion_dag.py` | Per-store fault isolation, chardet encoding detection, quarantine logic |
| `dbt/stg_pos_transactions.sql` | Bronze → Silver: SAFE_CAST, dedup via `row_number`, incremental MERGE |
| `great_expectations/pos_suite.py` | DQ checks: nulls, uniqueness, revenue range, row count freshness |
| `dags/alert_callback.py` | SLA miss → PagerDuty P1 + Slack #data-incidents |

> Speaker note: Briefly show one file if time allows — the DAG's per-store try/except is the most visually readable.

---

### Slide 13 — D11: Cost and Risk
**$20K–$33K/month. One dominant cost driver.**

| Component | Monthly Estimate |
|-----------|-----------------|
| BigQuery | $4,000–$8,000 |
| GCS / S3 | $2,000–$3,500 |
| Kafka | $3,000–$5,000 |
| Airflow | $2,000–$3,000 |
| **AWS Transcribe** | **$8,000–$12,000** |
| DataHub + Redis | $1,000–$2,000 |
| **Total** | **~$20,000–$33,500** |

**Audio transcription = 40% of total cost.** Mitigation: selective transcription (escalated calls only) → reduce by ~60%.

**Top 3 risks:**
1. **POS schema drift** (High/High) → schema evolution tests in CI, unknown columns quarantined
2. **Kafka consumer lag spike** (Medium/Medium) → auto-scaling consumer group, 7-day retention for replay
3. **GDPR erasure misses a table** (Low/Critical) → DataHub lineage + quarterly erasure drill + Legal audit

---

### Slide 14 — Concrete Questions (rapid-fire)
**8 questions the platform answers**

1. How does data flow from each source? → D2 ingestion table + architecture diagram
2. Where does each dataset live and why? → D3 storage table
3. How do you prevent double-counting on re-runs? → Bronze overwrite partitions + Silver MERGE
4. How do you identify one customer across 10 sources? → `customer_uuid` via deterministic + Splink
5. How do you find every row about customer X in <1 hour for GDPR? → DataHub lineage API → erasure macro
6. Which datasets are most sensitive? → Support call transcripts (Restricted), customer PII (Confidential)
7. If Finance dashboard is missing at 7 AM — what happens? → Airflow SLA callback → PagerDuty P1 → runbook
8. What would this cost to run? → ~$20K–$33K/month; audio is the lever

---

### Slide 15 — Architecture Recap (one-page visual)
**Show the full Mermaid diagram**

- Walk through it one more time end-to-end: Sources → Ingestion → Bronze → Silver → Gold → Consumers
- Point to: Kafka path (streaming), Airflow path (batch), Transcribe path (audio)
- Point to: Feature store branch (Feast + Redis) serving Data Science + Customer Success

> Speaker note: This is the visual anchor. If they remember one slide, it should be this one.

---

### Slide 16 — Close
**NorthBay goes from zero infrastructure to an enterprise-grade platform**

- 10 sources ingested reliably and idempotently
- One trusted customer identity across all systems
- Finance gets their 7 AM dashboard. Data Science has a feature store. Legal has a GDPR runbook.
- ~$20K–$33K/month — with a clear cost lever on audio
- Every design decision is auditable, every dataset has an owner, every alert has a runbook

**The platform is not just built — it's operable.**

---

## Timing Guide (15–20 min)

| Section | Slides | Target Time |
|---------|--------|-------------|
| Problem + philosophy | 1–3 | 2 min |
| Architecture + ingestion + storage | 4–6 | 4 min |
| Data quality + curation + governance | 7–9 | 4 min |
| Security + monitoring + artifacts | 10–12 | 4 min |
| Cost, risks, concrete Qs, close | 13–16 | 4 min |
| **Total** | **16 slides** | **~18 min** |
