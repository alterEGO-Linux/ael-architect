from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    blocking: bool=True

@dataclass
class ActionResult:
    success: bool
    message: str
    checks: list[Check]=field(default_factory=list)
    changed: bool=False

@dataclass
class AddonReport:
    name: str
    description: str
    enabled: bool
    visible: bool
    state: str

class Addon(ABC):
    name=""; description=""
    def __init__(self,config: dict,packages=None): self.config=config; self.packages=packages
    @property
    def enabled(self): return bool(self.config.get("enabled",False))
    @property
    def visible(self):
        return bool(self.config.get("visible", True))
    @property
    def state(self): return self.config.get("state","none")
    @abstractmethod
    def checks(self): raise NotImplementedError
    @abstractmethod
    def install(self): raise NotImplementedError
    @abstractmethod
    def enable(self): raise NotImplementedError
    @abstractmethod
    def disable(self): raise NotImplementedError
    def report(self):
        return AddonReport(
            self.name,
            self.description,
            self.enabled,
            self.visible,
            self.state
        )
