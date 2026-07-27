from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class AccessAuditEvent:
    actor_id: str
    actor_role: str
    resource_type: str
    resource_id: str
    purpose: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
