import json

from kafka import KafkaProducer

from app.events.models import AffirmationGeneratedEvent
from app.events.publisher import EventPublisher


class KafkaEventPublisher(EventPublisher):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            acks="all",
            retries=5,
            key_serializer=lambda value: value.encode("utf-8"),
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def publish(self, event: AffirmationGeneratedEvent) -> None:
        future = self.producer.send(
            self.topic,
            key=event.event_id,
            value=event.model_dump(mode="json"),
        )
        future.get(timeout=10)
