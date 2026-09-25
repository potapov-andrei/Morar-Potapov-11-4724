# ЛР1: AuditEvent вместо словаря.
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AuditEvent:

    event_id: str
    event_type: str
    entity_id: str
    timestamp: datetime
    details: dict


def describe(self):
        return f"{self.event_id}:{self.event_type}:{self.entity_id}"