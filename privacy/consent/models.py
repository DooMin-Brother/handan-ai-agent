from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class ConsentRecord:
    user_id: str
    policy_type: str
    policy_version: str
    agreed: bool
    agreed_at: datetime | None = None
    withdrawn_at: datetime | None = None

    @classmethod
    def agree(cls, user_id: str, policy_type: str, policy_version: str):
        return cls(
            user_id=user_id,
            policy_type=policy_type,
            policy_version=policy_version,
            agreed=True,
            agreed_at=datetime.now(timezone.utc),
        )
