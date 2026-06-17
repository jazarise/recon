class ReconXError(Exception):
    """Base exception for all ReconX errors."""
    pass

class ValidationError(ReconXError):
    """Raised when input validation fails."""
    pass

class PluginError(ReconXError):
    """Raised when a plugin encounters an error or fails to load."""
    pass

class WorkflowError(ReconXError):
    """Raised for workflow execution and validation errors."""
    pass

class DnsError(ReconXError):
    """Raised for DNS resolution failures."""
    pass

class HttpError(ReconXError):
    """Raised for HTTP client failures."""
    pass

class ConfigurationError(ReconXError):
    """Raised for configuration and setup issues."""
    pass

class ReportError(ReconXError):
    """Raised when report generation or exporting fails."""
    pass
