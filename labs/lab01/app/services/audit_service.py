from app.support.types import find_events
from app.support.types import Repository
from app.domain.audit import AuditEvent


def make_entity(event_id, event_type, entity_id, timestamp, details):
    return dict(
        event_id=event_id,
        event_type=event_type,
        entity_id=entity_id,
        timestamp=timestamp,
        details=dict(details)
    )


def _new_legacy_service(repository):
    return {
        "repository": repository
    }


def view(event):
    return dict(event)


def invoke(service, method, *args, **kwargs):

    if isinstance(service, AuditService):

        if method == "record":
            return service.record(args[0])

        if method == "find":
            return service.find(*args, **kwargs)

        if method == "render":
            return service.render(*args, **kwargs)

        raise ValueError(method)


    repository = service["repository"]

    if method == "record":
        return repository.add(args[0])

    events = find_events(repository.all(), *args, **kwargs)

    if method == "find":
        return events

    if method == "render":
        return tuple(
            f"{e['event_id']}|{e['event_type']}|{e['entity_id']}"
            for e in events
        )

    raise ValueError(method)

class AuditService:

    def __init__(self):
        self.events = []


    def record(self, event):

        if isinstance(event, dict):
            event = AuditEvent(
                event["event_id"],
                event["event_type"],
                event["entity_id"],
                event["timestamp"],
                event["details"]
            )


        for old_event in self.events:

            if old_event.event_id == event.event_id:
                raise Exception("DUPLICATE_EVENT")


        self.events.append(event)


    def find(
            self,
            entity_id=None,
            event_type=None
    ):

        result = []

        for event in self.events:

            if entity_id is not None:

                if event.entity_id != entity_id:
                    continue


            if event_type is not None:

                if event.event_type != event_type:
                    continue


            result.append(event)


        return tuple(result)


    def render(
            self,
            entity_id=None,
            event_type=None
    ):

        events = self.find(
            entity_id,
            event_type
        )

        return tuple(
            f"{event.event_id}|{event.event_type}|{event.entity_id}"
            for event in events
        )


def new_service(repository=None):

    if repository is not None:
        return _new_legacy_service(repository)

    return AuditService()