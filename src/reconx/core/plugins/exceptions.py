class PluginError(Exception):
    pass


class PluginValidationError(PluginError):
    pass


class PluginExecutionError(PluginError):
    pass


class PluginTimeoutError(PluginError):
    pass


class PluginPermissionError(PluginError):
    pass
