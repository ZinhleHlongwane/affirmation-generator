import json
import os

from kafka import KafkaConsumer

topic = os.getenv("KAFKA_TOPIC", "affirmation-events")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="affirmation-console-consumer",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print(f"Listening on {topic}...")

for message in consumer:
    event = message.value
    print(
        f"{event.get('event_type')} | "
        f"category={event.get('category')} | "
        f"source={event.get('source')}"
    )
