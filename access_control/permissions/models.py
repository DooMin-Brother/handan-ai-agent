from dataclasses import dataclass

@dataclass(frozen=True)
class AccessRequest:
    actor_id: str
    actor_role: str
    resource_type: str
    resource_id: str
    purpose: str | None = None

@dataclass(frozen=True)
class AccessDecision:
    allowed: bool
    reason: str
