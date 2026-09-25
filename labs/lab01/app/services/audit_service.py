from app.domain.audit import AuditEvent
from app.support.types import Repository, find_events


class AuditService:
    def __init__(self, repository):
        self._repository = repository

    def record(self, event):
        return self._repository.add(event)

    def find(self, entity_id=None, event_type=None):
        return find_events(
            self._repository.all(),
            entity_id=entity_id,
            event_type=event_type,
        )

    def render(self, entity_id=None, event_type=None):
        return tuple(
            f"{event.event_id}|{event.event_type}|{event.entity_id}"
            for event in self.find(entity_id=entity_id, event_type=event_type)
        )


def make_entity(event_id, event_type, entity_id, timestamp, details):
    return AuditEvent(event_id, event_type, entity_id, timestamp, details)


def view(event):
    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "entity_id": event.entity_id,
        "timestamp": event.timestamp,
        "details": event.details,
    }


def invoke(service, method, *args, **kwargs):
    if method == "record":
        return service.record(*args, **kwargs)
    if method == "find":
        return service.find(*args, **kwargs)
    if method == "render":
        return service.render(*args, **kwargs)
    raise ValueError(method)


def new_service(repository=None):
    if repository is None:
        repository = Repository("event_id", "DUPLICATE_EVENT")
    return AuditService(repository)
