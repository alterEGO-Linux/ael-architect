from __future__ import annotations
from pathlib import Path
import tomllib
DEFAULT_CONFIG = Path("alterego.toml")

class ConfigManager:
    def __init__(self,path: str|Path=DEFAULT_CONFIG):
        self.path=Path(path).expanduser(); self.data={}; self.reload()
    def reload(self):
        if not self.path.exists(): raise FileNotFoundError(f"Configuration file not found: {self.path}")
        with self.path.open("rb") as f: self.data=tomllib.load(f)
        return self.data
    def addon_config(self,name): return self.data.get("addons",{}).get(name,{})
    def _set_addon_field(self,name,field,value):
        text=self.path.read_text(encoding="utf-8"); lines=text.splitlines(); header=f"[addons.{name}]"; in_section=False; replaced=False; insert_at=None
        for i,line in enumerate(lines):
            stripped=line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                if in_section: insert_at=i; break
                in_section=(stripped==header); continue
            if in_section and stripped.startswith(f"{field} "):
                indent=line[:len(line)-len(line.lstrip())]; rendered=("true" if value is True else "false" if value is False else f'"{value}"'); lines[i]=f"{indent}{field} = {rendered}"; replaced=True; break
        if not replaced:
            if insert_at is None: insert_at=len(lines)
            rendered=("true" if value is True else "false" if value is False else f'"{value}"'); lines.insert(insert_at,f"{field} = {rendered}")
        self.path.write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8"); self.reload()
    def set_addon_enabled(self,name,enabled): self._set_addon_field(name,"enabled",enabled)
    def set_addon_state(self,name,state):
        if state not in {"loaded","none"}: raise ValueError("Add-on state must be loaded or none")
        self._set_addon_field(name,"state",state)

def load_config(path: str|Path=DEFAULT_CONFIG): return ConfigManager(path).data
