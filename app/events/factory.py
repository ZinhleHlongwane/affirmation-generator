from app.core.config import Settings
from app.events.kafka_publisher import KafkaEventPublisher
from app.events.publisher import EventPublisher, NoOpPublisher


def create_event_publisher(settings: Settings) -> EventPublisher:
    if not settings.kafka_enabled:
        return NoOpPublisher()

    return KafkaEventPublisher(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        topic=settings.kafka_topic,
    )
