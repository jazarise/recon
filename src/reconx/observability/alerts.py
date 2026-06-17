# Simple alerting definitions/checks
# In a real environment, Prometheus/Alertmanager handles this.
# This serves as a stub for internal checks.


class AlertManager:
    def check_workflow_failure_rate(self, total_workflows: int, failed_workflows: int):
        if total_workflows == 0:
            return False
        rate = failed_workflows / total_workflows
        if rate > 0.20:
            return True
        return False

    def check_plugin_crash_loop(self, plugin_failures: int):
        if plugin_failures > 5:
            return True
        return False
