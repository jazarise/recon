import enum


class PluginPermission(str, enum.Enum):
    NETWORK_ACCESS = "network_access"
    FILESYSTEM_READ = "filesystem_read"
    FILESYSTEM_WRITE = "filesystem_write"
    REPORT_GENERATION = "report_generation"
    DATABASE_ACCESS = "database_access"
