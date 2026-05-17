#!/usr/bin/env python3
"""
Builds DSCI 504 NorthBay Pantry presentation in Google Slides.

Before running:
    gcloud auth application-default login --no-browser \
        --scopes=https://www.googleapis.com/auth/presentations,https://www.googleapis.com/auth/drive.file
"""
import sys
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive.file',
]

# ── Colors (RGB 0–1) ──────────────────────────────────────────────────────────
NAVY  = {'red': 0.102, 'green': 0.137, 'blue': 0.196}   # #1a2332
CYAN  = {'red': 0.000, 'green': 0.831, 'blue': 1.000}   # #00d4ff
LGRAY = {'red': 0.910, 'green': 0.918, 'blue': 0.929}   # #e8eaed
WHITE = {'red': 1.000, 'green': 1.000, 'blue': 1.000}
AMBER = {'red': 1.000, 'green': 0.800, 'blue': 0.200}   # #ffcc33

# ── Layout (EMU: 1 inch = 914400) ─────────────────────────────────────────────
SW, SH = 9144000, 5143500          # slide 10" × 5.625"
LM     = 457200                    # 0.5" left/right margin
BW     = SW - 2 * LM              # usable body width
TY     = 180000                    # title y
TH     = 720000                    # title height
BY     = 1020000                   # body y
BH     = SH - BY - 180000         # body height


def _e(n): return {'magnitude': n, 'unit': 'EMU'}
def _p(n): return {'magnitude': n, 'unit': 'PT'}
def _c(rgb): return {'opaqueColor': {'rgbColor': rgb}}
def _tf(x, y): return {'scaleX': 1, 'scaleY': 1, 'translateX': x, 'translateY': y, 'unit': 'EMU'}


# ── Request builders ──────────────────────────────────────────────────────────

def bg_req(sid, color=NAVY):
    return {'updatePageProperties': {
        'objectId': sid,
        'pageProperties': {'pageBackgroundFill': {'solidFill': {'color': {'rgbColor': color}}}},
        'fields': 'pageBackgroundFill'
    }}


def box(oid, page, text, x, y, w, h, color=LGRAY, size=16, bold=False, align='LEFT'):
    return [
        {'createShape': {
            'objectId': oid, 'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': page,
                'size': {'width': _e(w), 'height': _e(h)},
                'transform': _tf(x, y)
            }
        }},
        {'insertText': {'objectId': oid, 'text': text, 'insertionIndex': 0}},
        {'updateTextStyle': {
            'objectId': oid,
            'style': {'foregroundColor': _c(color), 'fontSize': _p(size), 'bold': bold},
            'textRange': {'type': 'ALL'},
            'fields': 'foregroundColor,fontSize,bold'
        }},
        {'updateParagraphStyle': {
            'objectId': oid,
            'style': {'alignment': align, 'lineSpacing': 125, 'spaceAbove': _p(2)},
            'textRange': {'type': 'ALL'},
            'fields': 'alignment,lineSpacing,spaceAbove'
        }}
    ]


def title(oid, page, text, size=32):
    return box(oid, page, text, LM, TY, BW, TH, CYAN, size, bold=True)


def body(oid, page, text, size=15, y=BY, h=BH):
    return box(oid, page, text, LM, y, BW, h, LGRAY, size)


def add_slide(sid):
    return {'createSlide': {
        'objectId': sid,
        'slideLayoutReference': {'predefinedLayout': 'BLANK'}
    }}


def run_batch(service, pid, reqs):
    if not reqs:
        return
    for i in range(0, len(reqs), 50):
        service.presentations().batchUpdate(
            presentationId=pid, body={'requests': reqs[i:i + 50]}
        ).execute()


# ── Slide content ─────────────────────────────────────────────────────────────

SLIDES = [
    # (id,  title_text,  body_text,  title_size,  body_size)
    ('s02', 'The Problem — $1.4B in Revenue, Zero Data Infrastructure',
     """\
160 stores across US + UK  ·  E-commerce  ·  Pantry Box meal-kit  ·  PantryPlus loyalty

10 data sources:
  Some streaming at 80,000 events/minute
  Some nightly CSV files with garbled headers
  Some WAV audio files from customer support calls

Finance can't see revenue until manually assembled
Customer Success doesn't know a caller's order history when they call in
Data Science can't train models — no consistent data access

→  This is a greenfield build at $1.4B enterprise scale.""", 30, 17),

    ('s03', 'Design Philosophy — Match Tool to Workload',
     """\
A single database cannot serve real-time streaming, sub-second dashboards, and 5-year model training simultaneously.

Three questions drove every decision:

  1.  What is the shape of the data?       Structured / semi-structured / binary
  2.  What is the access pattern?          Streaming / batch / sub-second lookup
  3.  Who owns the data and who can see it?

Engineering decisions are principled — not arbitrary.
Every technology choice can be traced to one of these three questions.""", 30, 17),

    ('s04', 'D1 — Reference Architecture: Bronze → Silver → Gold',
     """\
  10 Sources  →  Ingestion Layer  →  Bronze (GCS)  →  Silver (BigQuery)  →  Gold (BigQuery)  →  Consumers
                                           ↑                  ↑                    ↑
                                      Raw, immutable     Cleaned, validated    Business-ready
                                      never modified     bad rows quarantined   role-gated

Bronze (GCS)          Raw files, forever. The recovery layer — any downstream bug is fixed by reprocessing from here.
Silver (BigQuery)     dbt cleans, validates, deduplicates. Entity resolution produces one customer_uuid per person.
Gold (BigQuery)       Finance, Marketing, and Data Science query here. Access enforced by role.
Feature Store         Feast + Redis — ML features served in <5ms to meet the Customer Success 2-second SLA.

Orchestration:  Apache Airflow (batch pipelines)  +  Apache Kafka (streaming events)""", 28, 14),

    ('s05', 'D2 — Ingestion: 10 Sources, 3 Patterns',
     """\
STREAMING (real-time)
  Sources:  OLTP PostgreSQL (CDC), Mobile App Events, MongoDB Change Streams
  Tool:     Debezium → Kafka → Kafka Connect → Bronze

BATCH (scheduled)
  Sources:  Store POS CSV/SFTP, Salesforce, PantryPlus Loyalty, 4 Marketing Platforms, Supplier EDI
  Tool:     Apache Airflow — one DAG per source

EVENT-DRIVEN (continuous)
  Sources:  Customer Support Call WAV files
  Tool:     S3 event → SQS → Lambda → AWS Transcribe → BigQuery

KEY DECISIONS
  Fault isolation on POS     One Airflow task per store. One broken CSV → quarantine + alert. 159 stores continue.
  Idempotency everywhere     Bronze partitioned by source/YYYY/MM/DD/run_id. Re-runs overwrite same partition.
  Rate limiting              PantryPlus API capped at 60 req/min via token-bucket limiter in Airflow operator.""", 30, 14),

    ('s06', 'D3 — Storage Architecture: Right Tool for the Right Workload',
     """\
GCS / S3               Raw files, WAV audio, scraped HTML
                       Cheapest $/GB · no schema enforcement · handles any binary

Apache Kafka           In-flight events from OLTP, Mobile, MongoDB
                       Decouples producers from consumers · replay on failure · Schema Registry enforces Avro contracts

BigQuery (Silver/Gold) Cleaned tables, dashboards, analytical queries
                       Columnar · TB-scale · sub-second aggregations · dbt-native

Feast + Redis          Online ML feature store — <5ms feature lookup for Customer Success
                       BigQuery's 1–3 sec query latency violates the 2-second SLA; Redis solves it

Feast + BigQuery       Offline ML feature store — full history for training churn, forecast, recommender models

"Why not one system?"
  BigQuery can't store WAV files.  S3 can't answer SELECT SUM(revenue) GROUP BY store in milliseconds.
  Redis exists for one specific reason: to serve a single SLA that BigQuery cannot meet.""", 30, 14),

    ('s07', 'D4 — Curation: The Customer Identity Problem',
     """\
Same person — 6 different records across 6 systems:
  "ahmad.var@gmail.com"   in OLTP PostgreSQL
  "AHMAD VAR" + phone     in Salesforce
  "ahmadvar@gmail.com"    in PantryPlus loyalty (typo variant)
  Device ID only          in Mobile App
  Hashed email            in Marketing platforms
  Username (pseudonymous) in Customer Reviews

Entity Resolution Pipeline:
  1  Deterministic pass     Exact match on normalized email → lower().strip() → same customer
  2  Probabilistic pass     Splink scoring: name + phone Soundex + address zip ≥ 0.85 → merge candidate
  3  Golden record          One customer_uuid (UUID v4) written to golden_customer_master
  4  Survivorship rule      Most recently updated non-null field wins · OLTP email is canonical

Also:
  golden_product_master     Flattens MongoDB nested attrs · standardizes allergen codes (FALCPA) · maps supplier hierarchy
  All amounts → USD         Daily ECB rate · original currency stored
  All timestamps → UTC      Display timezone applied at the query layer""", 28, 14),

    ('s08', 'D5 — Data Quality: Bad Data Has a Home, But Not in Production',
     """\
Schema conformance             Bronze · Great Expectations      → Quarantine file · Slack #data-alerts
Null rate on required fields   Silver · dbt not_null            → Block Silver load · PagerDuty P2
Duplicate primary keys         Silver · dbt unique              → Block load · alert
Row count ±20% vs prior day    Silver · dbt custom              → PagerDuty P1 if Finance table
Referential integrity (FK)     Silver · dbt relationships       → Log violation · do not block load
PII in non-PII table           Gold · GE custom expectation     → Block + incident ticket
Finance table immutability     Gold · audit trigger             → Block + SOX violation alert
Freshness SLA miss             Gold · Airflow SLA callback      → PagerDuty P1 if 7AM Finance miss

Quarantined rows land in bq_quarantine with reason code + timestamp. Never deleted — reviewed weekly by stewards.
Results surfaced in DataHub data quality dashboard visible to all owners and stewards.""", 28, 14),

    ('s09', 'D6 + D7 — Catalog and Governance',
     """\
DataHub (open-source catalog)
  Every column tagged:  domain · sensitivity (public/internal/confidential/restricted) · pii · source_system · owner
  Source-to-Gold lineage auto-ingested from dbt — full column-level lineage visible without manual effort
  PII tags flow: dbt meta:{pii:true} → DataHub → BigQuery column-level policy tag enforcement

Governance — 3 Roles, Clear Accountability
  Data Owner (VP)               Accountable for accuracy and access policy for their domain
  Data Steward (Analyst)        Reviews quarantine queue · approves schema change requests
  Data Custodian (Data Eng)     Implements access controls · runs and monitors pipelines

RACI Highlight
  golden_customer_master    Owner: VP Customer Success  |  Steward: CS Analyst    |  Legal: Consulted
  finance_daily_revenue     Owner: CFO                  |  Steward: Finance        |  Legal: Informed
  stg_call_transcripts      Owner: VP Customer Success  |  Steward: CS Analyst    |  Legal: ACCOUNTABLE

  Voice recordings are the only dataset where Legal is Accountable — not just Informed.""", 28, 14),

    ('s10', 'D8 — Security and Compliance: Two Frameworks, One Platform',
     """\
Access Controls
  BigQuery column-level policy tags:  call transcripts readable only by role:customer_success
  AES-256 at rest on all GCS + BigQuery  ·  WAV files use CMEK (customer-managed keys)  ·  TLS 1.3 in transit
  Cloud Audit Logs retained 7 years (SOX)
  SOX tables (finance_daily_revenue): append-only · no UPDATE/DELETE · change-controlled via dbt PR approval

GDPR Right-to-Erasure Runbook — target 5 business days, hard limit 30 days
  1  Look up customer_uuid in golden_customer_master using email or phone
  2  DataHub lineage API → lists every table containing customer_uuid FK in seconds
  3  Erasure dbt macro: nullify PII columns in Silver → replaces with [ERASED-{date}]
  4  Delete WAV files + transcripts from S3/BigQuery using call UUID index
  5  Submit deletion to Salesforce API + PantryPlus SaaS vendor APIs
  6  Bronze: PII stays (immutable raw) — permissible under GDPR audit exception · encrypted + access-restricted
  7  Log completion in gdpr_erasure_log table · notify customer within 30-day SLA

The DataHub lineage answer to "find every row about customer X" takes seconds, not hours.""", 28, 13),

    ('s11', 'D9 — Monitoring and Operations',
     """\
Pipeline SLAs
  Finance daily revenue     Available by 07:00 ET       P1 — page on-call immediately
  Store POS ingestion       Complete by 05:00 ET        P1 — Finance SLA depends on it
  Silver refresh            Complete by 06:00 ET        P1
  Customer 360 lookup       < 2 sec response            P2 — page within 15 min
  Loyalty / Marketing       Complete by 09:00 ET        P2

Alerting Chain
  Airflow SLA miss callback  →  PagerDuty (P1 or P2)  →  On-call data engineer  →  Slack #data-incidents

On-call: Weekly rotation among 3 engineers. Each DAG has a runbook_url tag — one click to the runbook.

Key Metrics
  DAG success rate per source · Bronze→Silver lag (minutes) · quarantine rate per source
  Kafka consumer lag · BigQuery slot utilization + cost per DAG · Gold table freshness

Cost tagging on every job: team / source_system / environment / dag_id → monthly VP-level cost reports""", 28, 14),

    ('s12', 'D10 — Sample Artifacts: The Design Is Backed by Working Code',
     """\
artifacts/dags/pos_ingestion_dag.py
  Per-store fault isolation via try/except — one broken file can't stop the other 159 stores
  chardet for encoding detection · quarantine bucket + Slack alert on failure

artifacts/dbt/stg_pos_transactions.sql
  Bronze → Silver transformation: SAFE_CAST on all columns · dedup via row_number()
  Incremental MERGE on natural key — guarantees idempotency

artifacts/great_expectations/pos_suite.py
  DQ checks: nulls on required fields · unique transaction IDs · revenue in valid range
  Row count freshness check — fails if today's batch is missing

artifacts/dags/alert_callback.py
  SLA miss callback: fires PagerDuty P1 payload + posts to Slack #data-incidents automatically
  Includes last-success timestamp in the alert so on-call engineer has immediate context

Each artifact demonstrates a different layer of the platform.
The per-store try/except in the DAG is the most readable illustration of fault isolation.""", 28, 15),

    ('s13', 'D11 — Cost and Risk: ~$20K–$33K/month',
     """\
BigQuery (storage + queries)      $4,000 – $8,000 /month
GCS / S3 (Bronze + audio)         $2,000 – $3,500 /month
Kafka (Confluent Cloud)           $3,000 – $5,000 /month
Airflow (Cloud Composer)          $2,000 – $3,000 /month
AWS Transcribe (250 hrs/day)      $8,000 – $12,000 /month   ← DOMINANT COST (40% of total)
DataHub + Redis                   $1,000 – $2,000  /month
TOTAL                            ~$20,000 – $33,500 /month

Mitigation: Transcribe only escalated calls → reduce audio cost by ~60%

Top 3 Risks
  HIGH probability / HIGH impact     POS schema drift breaks Silver
                                     → Schema evolution tests in CI · unknown columns quarantined on arrival

  MEDIUM / MEDIUM                    Kafka consumer lag during mobile event spike
                                     → Auto-scaling consumer group · 7-day topic retention for replay

  LOW probability / CRITICAL impact  GDPR erasure misses a table
                                     → DataHub lineage + quarterly erasure drill + Legal audit of erasure log""", 28, 13),

    ('s14', '8 Concrete Questions — Rapid Fire',
     """\
1   How does data flow from each source?
    D2 ingestion table — 3 patterns, 10 sources, specific tool for each

2   Where does each dataset live and why?
    D3 storage table — each system exists because no other system can do its job

3   How do you prevent double-counting on re-runs?
    Bronze overwrite partitions (source/YYYY/MM/DD/run_id) + Silver MERGE on natural key

4   How do you identify one customer across 10 sources?
    customer_uuid via deterministic email match first, then Splink probabilistic scoring

5   How do you find every row about customer X in under one hour for GDPR?
    DataHub lineage API lists all tables with customer_uuid FK in seconds → erasure macro runs in minutes

6   Which datasets are most sensitive and how is access controlled?
    Support call transcripts (Restricted) + customer PII (Confidential) — BigQuery column-level policy tags

7   If Finance dashboard is missing at 7 AM — what happens?
    Airflow SLA miss callback → PagerDuty P1 → on-call engineer with runbook URL in the alert

8   What would this cost to run?
    ~$20K–$33K/month · audio transcription is the cost lever (40% of total, reducible by 60%)""", 30, 16),

    ('s15', 'Architecture Recap — End to End',
     """\
  ┌─────────────────────────────────────────────────────────────────────────────────────────┐
  │  10 Sources  →  Ingestion Layer  →  Bronze (GCS)  →  Silver (BigQuery)  →  Gold (BigQuery) │
  └─────────────────────────────────────────────────────────────────────────────────────────┘
         │                   │                 │                  │                   │
    Kafka path          Airflow path       Raw files          dbt models          Business tables
    (streaming)          (batch)           immutable        + Great Exp.         Finance · Mktg
    OLTP, Mobile,       POS, EDI,          forever          quarantine bad         DS queries
    MongoDB             Salesforce                           rows, never delete
         │
    Transcribe path                                                            Feature Store
    (audio events)                                                             Feast + Redis
    WAV → S3 → Lambda → AWS Transcribe                                         <5ms online
    → BigQuery transcripts                                                       lookup

Key paths:
  Real-time events  →  Kafka  →  Kafka Connect  →  Bronze  →  Silver streaming model
  Daily batches     →  Airflow DAGs (one per source)  →  Bronze  →  dbt Silver  →  Gold
  Audio calls       →  S3 event trigger  →  Lambda  →  AWS Transcribe  →  BigQuery

Full annotated diagram: diagrams/architecture.mmd""", 30, 13),

    ('s16', 'NorthBay — From Zero Infrastructure to Enterprise-Grade Platform',
     """\
10 sources ingested reliably and idempotently
One trusted customer identity across all systems
Finance gets their 7 AM dashboard — every day, with an automated runbook if it's ever late
Data Science has a feature store with sub-millisecond online feature serving
Legal has a GDPR runbook that completes in 5 business days — not weeks
~$20K–$33K/month — with a clear cost lever on audio transcription

Every design decision is auditable.
Every dataset has an owner.
Every alert has a runbook.

The platform is not just built — it's operable.""", 28, 19),
]


def build_presentation():
    try:
        creds, project = google.auth.default(scopes=SCOPES)
    except google.auth.exceptions.DefaultCredentialsError:
        print("ERROR: No credentials found.")
        print("Run: gcloud auth application-default login --no-browser "
              "--scopes=https://www.googleapis.com/auth/presentations,"
              "https://www.googleapis.com/auth/drive.file")
        sys.exit(1)

    # Warn if service account (won't have access to user's Drive)
    if hasattr(creds, 'service_account_email'):
        print("WARNING: Detected service account credentials.")
        print("Google Slides requires your personal Google account.")
        print("Run: gcloud auth application-default login --no-browser "
              "--scopes=https://www.googleapis.com/auth/presentations,"
              "https://www.googleapis.com/auth/drive.file")
        sys.exit(1)

    service = build('slides', 'v1', credentials=creds)

    # Create presentation
    pres = service.presentations().create(body={
        'title': 'NorthBay Pantry — Enterprise Data Platform | DSCI 504'
    }).execute()
    pid = pres['presentationId']
    s1_id = pres['slides'][0]['objectId']
    print(f'Created presentation: {pid}')

    # Add slides 2–16
    run_batch(service, pid, [add_slide(s[0]) for s in SLIDES])

    # Set dark navy background on all slides
    all_ids = [s1_id] + [s[0] for s in SLIDES]
    run_batch(service, pid, [bg_req(sid) for sid in all_ids])

    # Delete default content on slide 1
    pres_data = service.presentations().get(presentationId=pid).execute()
    del_reqs = [
        {'deleteObject': {'objectId': el['objectId']}}
        for el in pres_data['slides'][0].get('pageElements', [])
    ]
    if del_reqs:
        run_batch(service, pid, del_reqs)

    # Build SLIDE 1 — Title slide
    content = []
    content += box('s1_name', s1_id,
                   'NorthBay Pantry\nEnterprise Data Platform',
                   LM, 1100000, BW, 1300000, CYAN, 52, bold=True, align='CENTER')
    content += box('s1_sub', s1_id,
                   'Designing an Enterprise Data Platform from Scratch',
                   LM, 2600000, BW, 500000, WHITE, 22, align='CENTER')
    content += box('s1_byline', s1_id,
                   'DSCI 504  ·  UBA MADS  ·  Ahmad Var  ·  May 2026',
                   LM, 3300000, BW, 450000, LGRAY, 18, align='CENTER')

    # Build slides 2–16
    for sid, t_text, b_text, t_size, b_size in SLIDES:
        content += title(f'{sid}_t', sid, t_text, t_size)
        content += body(f'{sid}_b', sid, b_text, b_size)

    run_batch(service, pid, content)

    url = f'https://docs.google.com/presentation/d/{pid}/edit'
    print(f'\nDone! Open your presentation:\n{url}')
    return url


if __name__ == '__main__':
    build_presentation()
