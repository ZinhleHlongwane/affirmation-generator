# ✨ Affirmation Intelligence Platform

An advanced portfolio project that combines **AI engineering, backend development, event streaming, data engineering, big-data processing, AWS cloud services and DevOps** around a simple product idea: personalised affirmations.

## What this project demonstrates

- Python
- FastAPI REST APIs
- AI-generated personalised affirmations
- Apache Kafka event streaming
- Apache Spark Structured Streaming
- ETL and medallion architecture
- Bronze / Silver / Gold data layers
- Amazon S3 data lake
- Amazon DynamoDB
- Docker and Docker Compose
- AWS ECS/Fargate infrastructure
- Terraform
- GitHub Actions CI
- Automated tests

---

# Architecture

```text
                         ┌────────────────────┐
                         │       User         │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │      FastAPI       │
                         │  REST API + AI     │
                         └─────────┬──────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
                 ▼                                   ▼
        ┌─────────────────┐                ┌──────────────────┐
        │ SQLite/Postgres │                │ Apache Kafka     │
        │ operational DB  │                │ event stream     │
        └─────────────────┘                └─────────┬────────┘
                                                    │
                                                    ▼
                                         ┌─────────────────────┐
                                         │ Spark Structured    │
                                         │ Streaming           │
                                         └─────────┬───────────┘
                                                   │
                      ┌────────────────────────────┼────────────────────────────┐
                      │                            │                            │
                      ▼                            ▼                            ▼
               ┌─────────────┐              ┌─────────────┐              ┌─────────────┐
               │   Bronze    │              │   Silver    │              │    Gold     │
               │ raw events  │────────────▶ │ clean data  │────────────▶ │ aggregates  │
               └──────┬──────┘              └─────────────┘              └──────┬──────┘
                      │                                                           │
                      ▼                                                           ▼
               ┌─────────────┐                                           ┌────────────────┐
               │ Amazon S3   │                                           │ DynamoDB       │
               │ data lake   │                                           │ live metrics   │
               └─────────────┘                                           └────────────────┘
```

---

# Main flow

1. A user sends a request to the FastAPI service.
2. The AI service generates a personalised affirmation.
3. The request and result are saved to the operational database.
4. An `affirmation.generated` event is published to Kafka.
5. Spark Structured Streaming consumes Kafka events.
6. Spark validates and transforms the events.
7. Raw, clean and aggregated data is written into Bronze, Silver and Gold layers.
8. The same layers can be uploaded to Amazon S3.
9. Gold metrics can be written to DynamoDB for low-latency access.
10. The API can be containerised and deployed to AWS ECS/Fargate.

---

# Event example

```json
{
  "event_id": "2de53416-d663-41b4-9027-4ad78eb15865",
  "event_type": "affirmation.generated",
  "affirmation_id": 21,
  "name": "Zinhle",
  "mood": "nervous",
  "goal": "become a confident software developer",
  "category": "career",
  "tone": "encouraging",
  "source": "openai",
  "affirmation": "I can keep learning and moving toward the developer I want to become.",
  "created_at": "2026-09-29T10:00:00+00:00"
}
```

---

# Project structure

```text
affirmation-intelligence-platform/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── events/
│   │   ├── models.py
│   │   ├── publisher.py
│   │   └── kafka_publisher.py
│   ├── services/
│   │   ├── affirmation_service.py
│   │   └── ai_service.py
│   ├── main.py
│   └── schemas.py
│
├── streaming/
│   ├── spark_streaming.py
│   └── kafka_consumer.py
│
├── pipeline/
│   ├── batch_etl.py
│   └── quality.py
│
├── aws/
│   ├── s3_data_lake.py
│   └── dynamodb_repository.py
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── tests/
│   ├── test_ai_service.py
│   ├── test_api.py
│   ├── test_events.py
│   └── test_pipeline.py
│
├── data/
│   └── seed_affirmations.csv
│
├── .github/workflows/ci.yml
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── dashboard.py
├── Makefile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Quick start

## 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Windows:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

The application works without an OpenAI API key. In that case it uses a deterministic fallback generator.

## 4. Start Kafka

```bash
docker compose up -d kafka
```

## 5. Start the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 6. Generate an affirmation

POST:

```text
/api/v1/affirmations/generate
```

Example body:

```json
{
  "name": "Zinhle",
  "mood": "nervous",
  "goal": "grow as a data engineer",
  "category": "career",
  "tone": "encouraging"
}
```

## 7. Inspect Kafka events

```bash
python -m streaming.kafka_consumer
```

## 8. Run Spark Structured Streaming

Spark needs the Kafka connector package:

```bash
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  streaming/spark_streaming.py
```

The Spark job produces:

```text
data/lake/bronze/
data/lake/silver/
data/lake/gold/
```

## 9. Run batch ETL

```bash
python -m pipeline.batch_etl
```

## 10. Run dashboard

```bash
streamlit run dashboard.py
```

---

# AWS

## S3

The `aws/s3_data_lake.py` module can upload Bronze, Silver and Gold outputs to:

```text
s3://<bucket>/bronze/
s3://<bucket>/silver/
s3://<bucket>/gold/
```

## DynamoDB

The `aws/dynamodb_repository.py` module stores Gold-layer category metrics using a simple single-table pattern.

Example keys:

```text
PK: CATEGORY#career
SK: LATEST
```

## ECS/Fargate

Terraform creates:

- ECR repository
- ECS cluster
- Fargate task definition
- Fargate service
- CloudWatch log group
- IAM roles
- S3 bucket
- DynamoDB table
- Security group
- default-VPC subnet discovery

Typical deployment:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Then build and push your Docker image to the generated ECR repository and update `container_image`.

---

# Why Kafka + Spark?

Kafka handles **event ingestion and distribution**.

Spark Structured Streaming handles **distributed processing, transformation and aggregation**.

That gives the project a realistic separation between:

```text
Event transport → processing → storage → serving
```

rather than using technologies only for keywords.

---

# Bronze / Silver / Gold

## Bronze
Raw events with minimal changes.

## Silver
Validated events with:
- clean categories
- parsed timestamps
- valid affirmation text
- standardised sources
- derived event date

## Gold
Aggregated analytics such as:
- total generated affirmations
- AI vs fallback counts
- category popularity
- average ratings
- daily event volume

---

# API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/v1/affirmations/generate` | Generate affirmation |
| GET | `/api/v1/affirmations/history` | Recent generation history |
| POST | `/api/v1/affirmations/{id}/feedback` | Store rating |
| GET | `/api/v1/analytics/summary` | Operational summary |

---

# Interview summary

> I started with a basic Python affirmation generator and redesigned it as an event-driven AI and data engineering platform. FastAPI handles generation requests, the AI service produces personalised affirmations, Kafka carries generation events, and Spark Structured Streaming processes those events into Bronze, Silver and Gold datasets. The architecture uses S3 as the cloud data lake and DynamoDB for low-latency metrics, while Docker, Terraform, GitHub Actions and ECS/Fargate provide a deployment path.

---

# Possible future improvements

- Amazon MSK instead of self-managed Kafka
- PostgreSQL for production persistence
- Glue Data Catalog
- Athena queries over S3
- Redshift for warehouse analytics
- schema registry with Avro
- dead-letter topic
- transactional outbox pattern
- Spark checkpoints in S3
- authentication
- scheduled personalised affirmations
