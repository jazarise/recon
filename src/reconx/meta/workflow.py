import logging

logger = logging.getLogger("reconx_meta")

class WorkflowEvolver:
    def __init__(self):
        self.current_sequence = ["dns_enum", "port_scan", "tech_detect"]

    def mutate_workflow(self, disabled_plugins: list) -> list:
        new_seq = [p for p in self.current_sequence if p not in disabled_plugins]
        
        # Meta-logic: if we drop port scanning, shift tech_detect earlier
        if "port_scan" in disabled_plugins and "tech_detect" in new_seq:
            logger.warning("[META-WORKFLOW] Evolutionary shift: Bypassing port_scan and promoting tech_detect.")
            new_seq.remove("tech_detect")
            new_seq.insert(0, "tech_detect")
            
        self.current_sequence = new_seq
        return self.current_sequence
