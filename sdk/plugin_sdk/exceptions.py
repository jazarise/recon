class PluginExecutionError(Exception):
    """Raised when a plugin fails to execute its underlying tool."""

    pass


class PluginValidationError(Exception):
    """Raised when a plugin fails validation (e.g., missing dependencies)."""

    pass
