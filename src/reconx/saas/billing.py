import logging

logger = logging.getLogger("reconx")

class BillingEngine:
    USAGE = {
        "org_1": {"plan": "Enterprise", "scans_used": 500, "limit": 99999},
        "org_2": {"plan": "Free", "scans_used": 1, "limit": 1}
    }

    @classmethod
    def can_dispatch_job(cls, tenant_id: str) -> bool:
        if tenant_id not in cls.USAGE:
            logger.error(f"[BILLING] Tenant {tenant_id} not registered in billing matrix.")
            return False
            
        data = cls.USAGE[tenant_id]
        if data["scans_used"] >= data["limit"]:
            logger.critical(f"[BILLING] Tenant {tenant_id} exceeded plan limits ({data['plan']}). Requires upgrade.")
            return False
            
        cls.USAGE[tenant_id]["scans_used"] += 1
        return True
