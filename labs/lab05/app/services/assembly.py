from app.domain.formatters import TextAuditFormatter, JsonAuditFormatter
from app.services.audit_service import AuditService
from app.support.types import Repository, choice


def build_service(repository=None, formatter=None, mode="text"):
    choices = {"text": TextAuditFormatter, "json": JsonAuditFormatter}
    choice(mode, choices, "INVALID_CONFIG")
    if repository is None:
        repository = Repository("event_id", "DUPLICATE_EVENT")
    if formatter is None:
        formatter = choices[mode]()
    return AuditService(repository, formatter)
