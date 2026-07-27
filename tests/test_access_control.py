from access_control.permissions.models import AccessRequest
from access_control.permissions.service import AccessControlService

def test_support_admin_allowed():
    result = AccessControlService().authorize(
        AccessRequest(
            actor_id="admin",
            actor_role="support_admin",
            resource_type="conversation",
            resource_id="session-1",
            purpose="기술지원",
        )
    )
    assert result.allowed is True

def test_user_denied_by_default():
    result = AccessControlService().authorize(
        AccessRequest(
            actor_id="user",
            actor_role="user",
            resource_type="conversation",
            resource_id="session-1",
        )
    )
    assert result.allowed is False
