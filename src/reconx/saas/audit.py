import logging
import datetime

logger = logging.getLogger("reconx_audit")


class ComplianceLogger:
    @staticmethod
    def log_action(tenant_id: str, user_role: str, action: str, target: str):
        timestamp = datetime.datetime.utcnow().isoformat()
        audit_entry = f"[{timestamp}] [TENANT: {tenant_id}] [ROLE: {user_role}] ACTION: {action} on {target}"
        logger.warning(audit_entry)  # Writes to compliance.log
