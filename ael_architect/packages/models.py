from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class PackageSpec:
    key: str
    enabled: bool
    visible: bool
    state: str
    name: str
    description: str
    category: str
    source: str
    package: str | None = None
    commands: list[str] = field(default_factory=list)
    url: str | None = None
    branch: str | None = None
    install: str | None = None
    remote: str | None = None

@dataclass
class PackageReport:
    key: str
    name: str
    description: str
    category: str
    source: str
    enabled: bool
    visible: bool
    state: str
    commands: list[str]
