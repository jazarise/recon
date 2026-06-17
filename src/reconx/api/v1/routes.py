from reconx.saas.auth import EnterpriseAuth
from reconx.saas.tenant import TenantContext
from reconx.saas.audit import ComplianceLogger
from reconx.saas.billing import BillingEngine
from reconx.api.websocket import streamer
import logging

logger = logging.getLogger("reconx")

class APIRouterV1:
    @staticmethod
    async def post_campaign(token: str, payload: dict):
        # 1. Auth & Context Resolution
        try:
            context = EnterpriseAuth.resolve_context(token)
            tenant_id = context["tenant_id"]
            role = context["role"]
            TenantContext.set_tenant(tenant_id)
        except ValueError as e:
            return {"status": 401, "error": str(e)}

        # 2. RBAC Validation
        if role == "Viewer":
            return {"status": 403, "error": "Viewers cannot mutate campaigns."}

        target = payload.get("target")

        # 3. Compliance Logging
        ComplianceLogger.log_action(tenant_id, role, "LAUNCH_CAMPAIGN", target)

        # 4. Billing Enforcement
        if not BillingEngine.can_dispatch_job(tenant_id):
            return {"status": 402, "error": "Payment Required / Usage Limit Exceeded"}

        # 5. Dispatch & Stream
        logger.info(f"[API V1] Dispatching Campaign for {tenant_id} on {target}")
        await streamer.broadcast_to_tenant(tenant_id, f"[Live] Campaign Initiated against {target}")

        return {"status": 202, "message": "Campaign Queued"}
