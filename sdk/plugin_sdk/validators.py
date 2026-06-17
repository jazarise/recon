import re


def validate_target(target: str) -> bool:
    """
    Validates that a target is a valid IP or hostname to prevent command injection.
    """
    # Simple regex for hostname or IP
    pattern = re.compile(r"^[a-zA-Z0-9.-]+$")
    return bool(pattern.match(target))
