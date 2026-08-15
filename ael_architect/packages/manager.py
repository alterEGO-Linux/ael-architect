from __future__ import annotations
from pathlib import Path
from threading import Lock
from ael_architect.addons.base import ActionResult, Check
from ael_architect.system.commands import command_exists, missing_commands
from .backends import PacmanBackend, AurBackend, GitBackend, SnapBackend, FlatpakBackend
from .catalog import PackageCatalog
from .models import PackageReport

BACKENDS = {
    "pacman": PacmanBackend(),
    "aur": AurBackend(),
    "git": GitBackend(),
    "snap": SnapBackend(),
    "flatpak": FlatpakBackend(),
}

class PackageManager:
    def __init__(self, path: str|Path):
        self.catalog = PackageCatalog(path)
        self._busy=set(); self._lock=Lock()

    def names(self): return self.catalog.names()
    def get(self, name): return self.catalog.get(name)
    def reports(self): return [self.report(name) for name in self.names()]
    def report(self, name):
        spec=self.get(name)
        return PackageReport(spec.key,spec.name,spec.description,spec.category,spec.source,spec.enabled,spec.visible,spec.state,spec.commands)

    def _acquire(self,name):
        with self._lock:
            if name in self._busy: return False
            self._busy.add(name); return True
    def _release(self,name):
        with self._lock: self._busy.discard(name)

    def health_check(self,name):
        spec=self.get(name)
        checks=[Check(cmd, command_exists(cmd), f"{cmd} found" if command_exists(cmd) else f"{cmd} not found") for cmd in spec.commands]
        actual="installed" if checks and all(c.ok for c in checks) else "uninstalled"
        if actual != spec.state: self.catalog.set_state(name, actual)
        return checks, actual

    def reconcile_enabled(self):
        results={}
        for name in self.names():
            spec=self.get(name)
            if spec.enabled and spec.state == "uninstalled":
                results[name]=self.install(name)
        return results

    def install(self,name):
        if not self._acquire(name):
            return ActionResult(success=False, message=f'"{name}" is already being installed.')
        try:
            spec=self.get(name)
            if spec.state == "installed":
                return ActionResult(success=True, changed=False, message=f'"{spec.name}" is already known as installed.')
            backend=BACKENDS.get(spec.source)
            if not backend:
                return ActionResult(success=False, message=f"Unknown package source: {spec.source}")
            result=backend.install(spec,self.catalog.settings)
            if not result.success: return result
            missing=missing_commands(spec.commands) if spec.commands else []
            if missing:
                return ActionResult(success=False, changed=result.changed, message="Installation completed, but commands are unavailable: "+", ".join(missing))
            self.catalog.set_state(name,"installed")
            return ActionResult(success=True, changed=True, message=f'"{spec.name}" installed successfully.')
        finally:
            self._release(name)

    def set_enabled(self,name,enabled):
        spec=self.get(name)
        self.catalog.set_enabled(name,enabled)
        if enabled and spec.state == "uninstalled":
            return self.install(name)
        return ActionResult(success=True, changed=True, message=(f'"{spec.name}" enabled.' if enabled else f'"{spec.name}" disabled in desired state. Uninstallation is not implemented yet.'))

    def ensure_command(self,command):
        spec=self.catalog.find_by_command(command)
        if spec is None:
            return ActionResult(success=False, message=f'No package providing "{command}" was found in packages.toml.')
        if spec.state == "installed":
            return ActionResult(success=True, changed=False, message=f'"{command}" is already known as available.')
        return self.install(spec.key)

    def sync_actual_state(self) -> dict[str, ActionResult]:

        results = {}

        for name in self.names():

            spec = self.get(name)

            checks, actual_state = self.health_check(
                name
            )

            actual_enabled = (
                actual_state == "installed"
            )

            changed = False

            if spec.state != actual_state:
                self.catalog.set_state(
                    name,
                    actual_state,
                )
                changed = True

            if spec.enabled != actual_enabled:
                self.catalog.set_enabled(
                    name,
                    actual_enabled,
                )
                changed = True

            results[name] = ActionResult(
                success=True,
                changed=changed,
                message=(
                    f'"{spec.name}" is {actual_state}.'
                ),
                checks=checks,
            )

        return results
