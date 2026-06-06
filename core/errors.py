class ReconXError(Exception):
    """Base exception for all ReconX errors."""
    pass

class PluginError(ReconXError):
    """Raised when a plugin fails execution."""
    pass

class WorkflowError(ReconXError):
    """Raised when a workflow configuration is invalid."""
    pass

class DependencyError(ReconXError):
    """Raised when dependency resolution fails or a required dependency is missing."""
    pass

class TimeoutError(ReconXError):
    """Raised when a task or plugin exceeds its allowed execution time."""
    pass
