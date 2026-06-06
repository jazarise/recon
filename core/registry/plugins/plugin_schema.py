from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class PluginType(str, Enum):
    NATIVE = "native"
    EXTERNAL = "external"
    HYBRID = "hybrid"

class PluginLifecycle(str, Enum):
    TESTING = "testing"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    BROKEN = "broken"
    ARCHIVED = "archived"

class Plugin(BaseModel):
    name: str
    version: str
    capability: str
    type: PluginType
    author: str
    entrypoint: str
    status: PluginLifecycle = PluginLifecycle.TESTING
    dependencies: List[str] = []
    
    class Config:
        use_enum_values = True
