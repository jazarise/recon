class IntelligenceError(Exception):
    pass


class NormalizationError(IntelligenceError):
    pass


class CorrelatorError(IntelligenceError):
    pass


class GraphInjectionError(IntelligenceError):
    pass
