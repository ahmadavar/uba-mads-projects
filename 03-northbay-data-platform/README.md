# DSCI 504 — NorthBay Pantry Enterprise Data Platform

**Course:** UBA MADS — DSCI 504  
**Due:** May 13, 2026  
**Author:** Ahmad Var

## Project Brief

Design an enterprise data platform for NorthBay Pantry — a $1.4B specialty grocery retailer with 160 stores (US + UK), e-commerce, a meal-kit subscription (Pantry Box), and a loyalty program (PantryPlus). The company has no existing data warehouse. This is a greenfield build.

## Repository Structure

```
03-northbay-data-platform/
├── report/
│   └── report.md              # Written report (≤3 pages, all 12 deliverables)
├── diagrams/
│   └── architecture.mmd       # Mermaid reference architecture diagram
├── artifacts/
│   ├── dags/                  # D10: Sample Airflow DAG
│   ├── dbt/                   # D10: Sample dbt model
│   └── great_expectations/    # D10: Sample GE validation suite
└── notebooks/
    └── northbay_platform.ipynb  # Design walkthrough notebook
```

## Deliverables Summary

| ID | Deliverable | Status |
|----|-------------|--------|
| D1 | Reference Architecture | ✅ |
| D2 | Per-Source Ingestion Design (10 sources) | ✅ |
| D3 | Storage Architecture | ✅ |
| D4 | Curation and Standardization Plan | ✅ |
| D5 | Data Quality Framework | ✅ |
| D6 | Metadata and Data Catalog | ✅ |
| D7 | Governance Model | ✅ |
| D8 | Security and Compliance Plan | ✅ |
| D9 | Monitoring and Operations | ✅ |
| D10 | Sample Artifacts (DAG, dbt, GE, alert) | ✅ |
| D11 | Cost and Risk Discussion | ✅ |
| D12 | Final Presentation | ✅ |

## Tech Stack Chosen

| Layer | Technology |
|-------|------------|
| Orchestration | Apache Airflow |
| Streaming | Apache Kafka + Schema Registry |
| Object Storage (Bronze) | Google Cloud Storage |
| Data Warehouse (Silver/Gold) | BigQuery |
| Transformation | dbt |
| Data Quality | Great Expectations |
| Feature Store | Feast + Redis |
| Catalog / Lineage | DataHub |
| Transcription | AWS Transcribe / OpenAI Whisper |
| CI/CD | GitHub Actions |
