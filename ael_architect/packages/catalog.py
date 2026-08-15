from __future__ import annotations
from pathlib import Path
import tomllib
from .models import PackageSpec

class PackageCatalog:
    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self.reload()

    def reload(self):
        if not self.path.is_file():
            raise FileNotFoundError(f"Package catalog not found: {self.path}")
        with self.path.open("rb") as file:
            self.data = tomllib.load(file)
        self.settings = self.data.get("settings", {})

    def names(self) -> list[str]:
        return sorted(self.data.get("packages", {}))

    def get(self, key: str) -> PackageSpec:
        data = self.data.get("packages", {}).get(key)
        if data is None:
            raise KeyError(f"Unknown package: {key}")
        return PackageSpec(
            key=key,
            enabled=bool(data.get("enabled", False)),
            visible=bool(data.get("visible", True)),
            state=data.get("state", "uninstalled"),
            name=data.get("name", key),
            description=data.get("description", ""),
            category=data.get("category", "Other"),
            source=data.get("source", "pacman"),
            package=data.get("package", key),
            commands=list(data.get("command", [])),
            url=data.get("url"),
            branch=data.get("branch"),
            install=data.get("install"),
            remote=data.get("remote"),
        )

    def find_by_command(self, command: str) -> PackageSpec | None:
        for key in self.names():
            spec = self.get(key)
            if command in spec.commands:
                return spec
        return None

    def _set_field(self, key: str, field: str, value: str | bool) -> None:
        text = self.path.read_text(encoding="utf-8")
        lines = text.splitlines()
        header = f"[packages.{key}]"
        in_section = False
        replaced = False
        insert_at = None
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                if in_section:
                    insert_at = index
                    break
                in_section = stripped == header
                continue
            if in_section and stripped.startswith(f"{field} "):
                indent = line[:len(line)-len(line.lstrip())]
                rendered = ("true" if value is True else "false" if value is False else f'"{value}"')
                lines[index] = f"{indent}{field} = {rendered}"
                replaced = True
                break
        if not replaced:
            if insert_at is None: insert_at = len(lines)
            rendered = ("true" if value is True else "false" if value is False else f'"{value}"')
            lines.insert(insert_at, f"{field} = {rendered}")
        self.path.write_text("\n".join(lines).rstrip()+"\n", encoding="utf-8")
        self.reload()

    def set_enabled(self, key: str, enabled: bool) -> None:
        self._set_field(key, "enabled", enabled)

    def set_state(self, key: str, state: str) -> None:
        if state not in {"installed", "uninstalled"}:
            raise ValueError("Package state must be installed or uninstalled")
        self._set_field(key, "state", state)
