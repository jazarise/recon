import yaml
import os
import graphlib
from typing import Dict, Any, List
from reconx.core.errors import WorkflowError, DependencyError
from reconx.core.logger import logger
from reconx.core.models.finding import Finding

class WorkflowContext:
    def __init__(self, target: str, scan_id: str):
        self.target = target
        self.scan_id = scan_id
        self.findings: List[Finding] = []
        self.variables: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {}

class WorkflowEngine:
    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = workflows_dir
        self.workflows: Dict[str, Any] = {}
        self.load_workflows()

    def load_workflows(self):
        if not os.path.exists(self.workflows_dir):
            return
        import glob
        pattern = os.path.join(self.workflows_dir, "**", "*.y*ml")
        for path in glob.glob(pattern, recursive=True):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data and isinstance(data, dict) and "name" in data:
                        self.workflows[data["name"]] = data
            except Exception as e:
                logger.error(f"Failed to load workflow {path}: {e}")

    def validate_workflow(self, workflow_name: str):
        if workflow_name not in self.workflows:
            raise WorkflowError(f"Workflow '{workflow_name}' not found.")
        # Future: validate plugins exist in registry
        return True

    def build_execution_graph(self, workflow_name: str) -> tuple[graphlib.TopologicalSorter, List[str]]:
        workflow = self.workflows[workflow_name]
        steps = workflow.get("steps", [])
        
        graph = {}
        all_plugins = []
        
        for step in steps:
            if isinstance(step, str):
                graph[step] = set()
                all_plugins.append(step)
            elif isinstance(step, dict):
                for plugin_name, config in step.items():
                    all_plugins.append(plugin_name)
                    depends_on = config.get("depends_on", []) if isinstance(config, dict) else []
                    graph[plugin_name] = set(depends_on)
                    
        sorter = graphlib.TopologicalSorter(graph)
        try:
            # Check for cycles
            list(graphlib.TopologicalSorter(graph).static_order())
        except graphlib.CycleError as e:
            raise DependencyError(f"Cycle detected in workflow '{workflow_name}': {e}")
            
        return sorter, all_plugins

workflow_engine = WorkflowEngine()
