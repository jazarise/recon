from reconx.core.security.auth import auth_system
from reconx.core.security.rbac import has_permission, PermissionDeniedError
from reconx.core.audit.audit_logger import audit_logger
from reconx.core.api_gateway.rate_limiter import rate_limiter


class GatewayRouter:
    def handle_request(
        self, token: str, endpoint: str, required_role: str, action: str, target: str
    ):
        """Unified API ingress that enforces all enterprise security controls."""
        # 1. Authenticate
        user_data = auth_system.decode_token(token)
        if not user_data:
            audit_logger.log(
                "UNKNOWN", action, target, "FAILED", "Invalid or expired token"
            )
            raise Exception("Unauthorized")

        user = user_data["sub"]
        role = user_data["role"]

        # 2. Rate Limit
        if not rate_limiter.is_allowed(user):
            audit_logger.log(user, action, target, "FAILED", "Rate limit exceeded")
            raise Exception("Too Many Requests")

        # 3. RBAC Authorization
        if not has_permission(role, required_role):
            audit_logger.log(
                user,
                action,
                target,
                "FAILED",
                f"Permission denied (requires {required_role})",
            )
            raise PermissionDeniedError("Forbidden")

        # 4. Audit Log
        audit_logger.log(user, action, target, "SUCCESS")

        return {"status": "success", "user": user, "action": action}


gateway = GatewayRouter()
