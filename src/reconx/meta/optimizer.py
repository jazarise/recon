import logging

logger = logging.getLogger("reconx_meta")

class PluginOptimizer:
    def __init__(self):
        self.plugin_stats = {
            "dns_enum": {"calls": 10, "yields": 8},
            "port_scan": {"calls": 10, "yields": 0} # Example failing plugin
        }

    def evaluate_plugins(self) -> list:
        disabled = []
        for plugin, stats in self.plugin_stats.items():
            if stats["calls"] >= 10:
                yield_rate = stats["yields"] / stats["calls"]
                if yield_rate < 0.05:
                    logger.critical(f"[META-OPTIMIZER] Plugin '{plugin}' yield rate ({yield_rate*100}%) is below 5%. Auto-disabling.")
                    disabled.append(plugin)
        return disabled
