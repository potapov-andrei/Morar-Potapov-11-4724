from app.domain.audit import AuditEvent
from app.domain.formatters import JsonAuditFormatter, TextAuditFormatter
from app.support.types import find_events, format_result


class AuditService:
    def __init__(self,repository,mode="text"):
        self._repository=repository
        self._mode=mode

    def record(self,event):
        return self._repository.add(event)

    def find(self,entity_id=None,event_type=None):
        return find_events(self._repository.all(),entity_id,event_type)

    def render(self,entity_id=None,event_type=None):
        formatter = JsonAuditFormatter() if self._mode == "json" else TextAuditFormatter()
        events = self.find(entity_id=entity_id,event_type=event_type)
        return tuple(format_result(formatter.format(event)) for event in events)

def make_entity(*args, **kwargs):
    return AuditEvent(*args, **kwargs)


def invoke(service, method, *args, **kwargs):
    return getattr(service, method)(*args, **kwargs)


def view(entity):
    return {'event_id': entity.event_id, 'event_type': entity.event_type, 'entity_id': entity.entity_id, 'timestamp': entity.timestamp, 'details': entity.details}


from app.support.types import Repository,choice

def new_service(repository=None,mode="text"):
    choice(mode,("text","json"),"INVALID_CONFIG")
    return AuditService(repository if repository is not None else Repository("event_id","DUPLICATE_EVENT"),mode)
