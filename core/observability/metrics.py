class Metrics:
    def __init__(self):
        self.scan_durations = []
        self.api_requests = 0
        self.plugin_failures = 0
        
    def record_scan(self, capability: str, duration: float):
        self.scan_durations.append({
            "capability": capability,
            "duration": duration
        })
        
    def record_api_request(self):
        self.api_requests += 1
        
    def get_metrics(self):
        avg_scan_time = sum(d["duration"] for d in self.scan_durations) / len(self.scan_durations) if self.scan_durations else 0
        return {
            "total_scans": len(self.scan_durations),
            "avg_scan_duration_sec": round(avg_scan_time, 2),
            "total_api_requests": self.api_requests,
            "plugin_failures": self.plugin_failures
        }

metrics = Metrics()
