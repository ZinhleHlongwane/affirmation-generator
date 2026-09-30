from abc import ABC, abstractmethod

from app.events.models import AffirmationGeneratedEvent


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: AffirmationGeneratedEvent) -> None:
        raise NotImplementedError


class NoOpPublisher(EventPublisher):
    def publish(self, event: AffirmationGeneratedEvent) -> None:
        return None
