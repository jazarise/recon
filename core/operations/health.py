class HealthMonitor:
    def get_metrics(self):
        return {
            "status": "Healthy",
            "cpu_usage": "15%",
            "memory_usage": "250MB",
            "queue_depth": 0
        }
