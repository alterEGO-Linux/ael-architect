from __future__ import annotations
from pathlib import Path
import re
from ael_architect.system.commands import command_path
from .base import Addon,ActionResult,Check

class ShowUtcAddon(Addon):
    name="show-utc"; description="Load the AlterEGO show-utc shell module."
    def __init__(self,config,packages=None):
        super().__init__(config,packages); self.ael_root=Path(config.get("ael_root","~/.ael")).expanduser(); self.modules_file=self.ael_root/".modules"; self.script_file=self.ael_root/"bin"/"show-utc"
    def _line_state(self):
        if not self.modules_file.is_file(): return "missing"
        text=self.modules_file.read_text(encoding="utf-8")
        if re.search(r'^\s*source_module\s+"\$\{AEL_BIN\}/show-utc"\s*$',text,re.M): return "active"
        if re.search(r'^\s*#\s*source_module\s+"\$\{AEL_BIN\}/show-utc"\s*$',text,re.M): return "inactive"
        return "missing-entry"
    def checks(self):
        bash=command_path("bash"); date=command_path("date"); state=self._line_state()
        return [
            Check("bash",bash is not None,bash or "bash is not installed"),
            Check("date",date is not None,date or "date is not installed"),
            Check("show-utc script",self.script_file.is_file(),str(self.script_file)),
            Check(".modules file",self.modules_file.is_file(),str(self.modules_file)),
            Check("source_module entry",state=="active",{"active":"show-utc entry is loaded","inactive":"show-utc entry is commented","missing":".modules does not exist","missing-entry":"show-utc source_module entry is missing"}[state]),
        ]
    def install(self):
        for command in ["bash","date"]:
            result=self.packages.ensure_command(command)
            if not result.success: return result
        if not self.script_file.is_file(): return ActionResult(success=False,message=f"show-utc script is missing:\n{self.script_file}")
        if not self.modules_file.is_file(): return ActionResult(success=False,message=f".modules is missing:\n{self.modules_file}")
        if self._line_state()=="missing-entry": return ActionResult(success=False,message="show-utc source_module entry is missing from .modules.")
        return ActionResult(success=True,changed=False,message='"show-utc" requirements are installed.')
    def enable(self):
        if self._line_state()=="active": return ActionResult(success=True,changed=False,message='"show-utc" is already loaded.')
        text=self.modules_file.read_text(encoding="utf-8")
        updated,count=re.subn(r'^(\s*)#\s*source_module\s+"\$\{AEL_BIN\}/show-utc"\s*$',r'\1source_module "${AEL_BIN}/show-utc"',text,count=1,flags=re.M)
        if count!=1: return ActionResult(success=False,message="Unable to load show-utc.")
        self.modules_file.write_text(updated,encoding="utf-8")
        return ActionResult(success=True,changed=True,message='"show-utc" loaded successfully.')
    def disable(self): return ActionResult(success=True,changed=False,message="Removal/unloading is not implemented yet.")
