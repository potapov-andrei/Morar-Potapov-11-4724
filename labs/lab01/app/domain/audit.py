from dataclasses import dataclass, field
from datetime import datetime

from app.support.types import EVENT_TYPES, choice, details_copy, identifier, utc_seconds


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    event_type: str
    entity_id: str
    timestamp: datetime
    _details: dict[str, str] = field(repr=False, hash=False)

    def __init__(self, event_id, event_type, entity_id, timestamp, details):
        object.__setattr__(self, "event_id", identifier(event_id))
        object.__setattr__(self, "event_type", choice(event_type, EVENT_TYPES))
        object.__setattr__(self, "entity_id", identifier(entity_id))
        object.__setattr__(self, "timestamp", utc_seconds(timestamp))
        object.__setattr__(self, "_details", details_copy(details))

    @property
    def details(self):
        return details_copy(self._details)

    def describe(self):
        return f"{self.event_id}:{self.event_type}:{self.entity_id}"
