from __future__ import annotations
from threading import Lock
from ael_architect.config import ConfigManager
from ael_architect.packages import PackageManager
from .base import ActionResult
from .show_utc import ShowUtcAddon
from .windows_11 import Windows11Addon
ADDONS={ShowUtcAddon.name:ShowUtcAddon,Windows11Addon.name:Windows11Addon}

class AddonManager:
    def __init__(self,config:ConfigManager):
        self.config=config; self.packages=PackageManager(config.path.with_name("packages.toml")); self._busy=set(); self._busy_lock=Lock()
    def names(self): return sorted(ADDONS)
    def get(self,name): return ADDONS[name](self.config.addon_config(name),self.packages)
    def reports(self): return [self.get(n).report() for n in self.names()]
    def _acquire(self,name):
        with self._busy_lock:
            if name in self._busy: return False
            self._busy.add(name); return True
    def _release(self,name):
        with self._busy_lock: self._busy.discard(name)
    def check(self,name):
        addon=self.get(name); checks=addon.checks(); actual="loaded" if checks and all(c.ok for c in checks if c.blocking) else "none"
        if actual != addon.state: self.config.set_addon_state(name,actual)
        return checks,actual
    def reconcile_all(self):
        results={f"package:{k}":v for k,v in self.packages.reconcile_enabled().items()}
        for name in self.names():
            addon=self.get(name)
            if addon.enabled and addon.state=="none": results[name]=self.set_enabled(name,True)
        return results
    def set_enabled(self,name,enabled):
        if not self._acquire(name): return ActionResult(success=False,message=f'"{name}" is already running.')
        try:
            addon=self.get(name); self.config.set_addon_enabled(name,enabled)
            if not enabled:
                return ActionResult(success=True,changed=True,message=f'"{name}" disabled in desired state. Removal/unloading is not implemented yet.')
            if addon.state=="loaded": return ActionResult(success=True,changed=False,message=f'"{name}" is already known as loaded.')
            result=addon.install()
            if not result.success: return result
            result=addon.enable()
            if result.success: self.config.set_addon_state(name,"loaded")
            return result
        finally: self._release(name)
