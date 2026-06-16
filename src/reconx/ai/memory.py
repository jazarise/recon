class ContextMemory:
    def __init__(self):
        self._scanned = set()
        self._failed = set()

    def mark_scanned(self, target: str):
        self._scanned.add(target)

    def mark_failed(self, target: str):
        self._failed.add(target)

    def should_scan(self, target: str) -> bool:
        if target in self._scanned or target in self._failed:
            return False
        return True
