from access_control.audit_log.models import AccessAuditEvent

class AuditLogService:
    def __init__(self) -> None:
        self._events: list[AccessAuditEvent] = []

    def record(self, event: AccessAuditEvent) -> None:
        self._events.append(event)

    def list_events(self) -> list[AccessAuditEvent]:
        return list(self._events)
