# ✨ Affirmation Intelligence Platform

An event-driven AI and data engineering platform that generates personalised affirmations and turns each generation request into streaming analytics data.

The project started as a simple Python affirmation generator and was redesigned into a multi-service platform using **FastAPI, Apache Kafka, Apache Spark, Docker, AWS and Terraform**.

It demonstrates how a small product idea can be extended into a realistic architecture covering API development, AI integration, event streaming, ETL, data lake design, analytics and cloud infrastructure.

---

# Architecture

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
        │     SQLite      │                │ Apache Kafka     │
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

---

# Main Flow

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

# Tech Stack

## Backend & AI

- Python
- FastAPI
- OpenAI integration
- SQLAlchemy
- REST APIs

## Data Engineering

- Apache Kafka
- Apache Spark Structured Streaming
- Batch ETL
- Bronze / Silver / Gold architecture
- Data quality validation
- Event-driven architecture

## Cloud & Infrastructure

- Amazon S3
- Amazon DynamoDB
- AWS ECS/Fargate
- Amazon ECR
- CloudWatch
- Terraform

## DevOps & Analytics

- Docker
- Docker Compose
- GitHub Actions
- Streamlit
- Pytest

---

# Event Example

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

---

# Project Structure

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
    │   │   ├── factory.py
    │   │   ├── kafka_publisher.py
    │   │   ├── models.py
    │   │   └── publisher.py
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
    ├── .github/
    │   └── workflows/
    │       └── ci.yml
    │
    ├── .env.example
    ├── .gitignore
    ├── docker-compose.yml
    ├── Dockerfile
    ├── dashboard.py
    ├── Makefile
    ├── PORTFOLIO_NOTES.md
    ├── pyproject.toml
    ├── requirements.txt
    └── README.md

---

# Quick Start

## 1. Create a Virtual Environment

    python -m venv .venv

Windows PowerShell:

    .venv\Scripts\Activate.ps1

macOS/Linux:

    source .venv/bin/activate

## 2. Install Dependencies

    pip install -r requirements.txt

## 3. Configure Environment Variables

Windows:

    Copy-Item .env.example .env

macOS/Linux:

    cp .env.example .env

The application can run without an OpenAI API key. In that case it uses a deterministic fallback affirmation generator.

## 4. Start Kafka

    docker compose up -d kafka

## 5. Start the API

    uvicorn app.main:app --reload

Open:

    http://127.0.0.1:8000/docs

## 6. Generate an Affirmation

Endpoint:

    POST /api/v1/affirmations/generate

Example request:

    {
      "name": "Zinhle",
      "mood": "nervous",
      "goal": "grow as a data engineer",
      "category": "career",
      "tone": "encouraging"
    }

## 7. Inspect Kafka Events

    python -m streaming.kafka_consumer

## 8. Run Spark Structured Streaming

Spark requires the Kafka connector package.

    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 streaming/spark_streaming.py

The streaming job writes data to:

    data/lake/bronze_stream/
    data/lake/silver_stream/
    data/lake/gold_stream/

Checkpoint data is stored under:

    data/lake/checkpoints/

## 9. Run Batch ETL

    python -m pipeline.batch_etl

## 10. Run the Dashboard

    streamlit run dashboard.py

---

# Data Pipeline

## Bronze

The Bronze layer stores raw streaming events with minimal transformation.

Typical contents include:

- Kafka key
- raw JSON payload
- Kafka timestamp

## Silver

The Silver layer contains validated and cleaned events.

Processing includes:

- filtering for `affirmation.generated` events
- validating affirmation text
- parsing timestamps
- standardising categories
- standardising event sources
- removing invalid records

## Gold

The Gold layer contains aggregated analytics such as:

- affirmation generation counts
- category-level generation activity
- AI vs fallback source activity
- time-windowed generation metrics

---

# Why Kafka + Spark?

Kafka is responsible for **event ingestion and distribution**.

Spark Structured Streaming is responsible for **distributed processing, transformation and aggregation**.

This creates a realistic separation between:

    Event transport → processing → storage → serving

rather than using technologies only as isolated tools.

---

# AWS Integration

## Amazon S3

The `aws/s3_data_lake.py` module can upload Bronze, Silver and Gold datasets to an S3 data lake.

Example structure:

    s3://<bucket>/bronze/
    s3://<bucket>/silver/
    s3://<bucket>/gold/

## Amazon DynamoDB

The `aws/dynamodb_repository.py` module can store Gold-layer metrics for low-latency access.

Example key design:

    PK: CATEGORY#career
    SK: LATEST

## ECS / Fargate

Terraform includes infrastructure for:

- Amazon ECR repository
- ECS cluster
- Fargate task definition
- Fargate service
- CloudWatch log group
- IAM roles
- Amazon S3 bucket
- DynamoDB table
- Security group
- default VPC subnet discovery

Typical Terraform workflow:

    cd terraform
    terraform init
    terraform plan
    terraform apply

After provisioning, the Docker image can be pushed to the generated ECR repository and referenced through the Terraform `container_image` variable.

> Note: Running `terraform apply` may create billable AWS resources.

---

# API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/v1/affirmations/generate` | Generate a personalised affirmation |
| GET | `/api/v1/affirmations/history` | Retrieve recent affirmation history |
| POST | `/api/v1/affirmations/{id}/feedback` | Store user feedback |
| GET | `/api/v1/analytics/summary` | Retrieve operational analytics |

---

# Testing

The project includes automated tests covering:

- AI affirmation generation
- API endpoints
- event publishing
- ETL and data quality logic

Run the full test suite with:

    pytest

---

# Continuous Integration

GitHub Actions runs the automated test suite on repository changes to help detect regressions.

Workflow:

    .github/workflows/ci.yml

---

# Docker

The project includes Docker support for the main application services.

To start Kafka:

    docker compose up -d kafka

To run the Spark streaming service through Docker Compose:

    docker compose up spark

The Docker setup uses separate Kafka listeners for host-based and container-based applications.

Host applications connect through:

    localhost:9092

Docker services connect through:

    kafka:29092

---

# Project Evolution

This project started as a basic Python affirmation generator focused on simple user input and motivational messages.

It was redesigned into an event-driven AI and data engineering platform.

The current architecture combines:

- FastAPI for REST API development
- AI-powered personalised generation
- SQLAlchemy for operational persistence
- Kafka for event streaming
- Spark Structured Streaming for real-time processing
- batch ETL for data transformation
- Bronze, Silver and Gold data layers
- S3 for cloud data lake storage
- DynamoDB for low-latency metrics
- Streamlit for analytics
- Docker for containerisation
- Terraform for infrastructure as code
- GitHub Actions for continuous integration

This evolution demonstrates how a small Python project can be expanded into a more realistic software and data engineering system.

---

# Possible Future Improvements

- Amazon MSK instead of self-managed Kafka
- PostgreSQL for production persistence
- AWS Glue Data Catalog
- Athena queries over S3
- Redshift for warehouse analytics
- Schema Registry with Avro
- dead-letter Kafka topic
- transactional outbox pattern
- Spark checkpoints stored in S3
- authentication and authorization
- scheduled personalised affirmations
- improved monitoring and observability
'@ | Set-Content -Path README.md -Encoding UTF8
