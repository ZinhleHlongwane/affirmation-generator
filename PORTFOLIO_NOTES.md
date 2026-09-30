# Portfolio Notes

## Technologies actually implemented

- FastAPI
- OpenAI integration with local fallback
- SQLAlchemy
- Kafka producer
- Kafka consumer
- Spark Structured Streaming
- batch ETL
- Bronze/Silver/Gold layers
- S3 upload abstraction
- DynamoDB repository
- Docker
- Docker Compose
- Terraform
- ECS/Fargate infrastructure
- GitHub Actions
- pytest

## Technologies intentionally not included

- Flink
- Hadoop
- Kinesis

They are not necessary for this project's architecture. Kafka + Spark already provide a clear and explainable event-streaming and big-data story.

## Recommended commit sequence

1. `refactor: rebuild affirmation generator as FastAPI service`
2. `feat: add personalised AI affirmation generation`
3. `feat: persist generation events with SQLAlchemy`
4. `feat: publish affirmation events to Kafka`
5. `feat: add Spark structured streaming pipeline`
6. `feat: implement bronze silver gold data layers`
7. `feat: add S3 data lake and DynamoDB metrics support`
8. `feat: add analytics dashboard`
9. `infra: add Docker and ECS Fargate Terraform`
10. `test: add API event and data pipeline tests`
11. `ci: add GitHub Actions test workflow`
