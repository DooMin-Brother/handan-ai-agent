from access_control.permissions.models import AccessDecision, AccessRequest

class AccessControlService:
    def authorize(self, request: AccessRequest) -> AccessDecision:
        if request.actor_role in {"system_admin", "support_admin"}:
            return AccessDecision(True, "개발 정책상 허용된 관리자 역할")
        return AccessDecision(False, "명시적 접근 권한이 없습니다.")
