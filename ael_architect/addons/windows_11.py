from __future__ import annotations

from pathlib import Path
import shutil

from .base import Addon, ActionResult, Check


class Windows11Addon(Addon):
    def __init__(self, config: dict, packages=None):
        super().__init__(config, packages)

    name = "windows-11"
    description = "Create and configure a Windows 11 VirtualBox virtual machine."

    def _vm(self) -> dict:
        return self.config.get("vm", {})

    def _install(self) -> dict:
        return self.config.get("install", {})

    def checks(self) -> list[Check]:
        vm = self._vm()
        install = self._install()
        iso_value = install.get("iso", "")
        iso = Path(iso_value).expanduser() if iso_value else None
        disk_gb = int(vm.get("disk_gb", 0))
        storage_path = Path(self.config.get("storage_path", "~/VirtualBox VMs")).expanduser()

        parent = storage_path
        while not parent.exists() and parent != parent.parent:
            parent = parent.parent

        try:
            free_gb = shutil.disk_usage(parent).free // (1024 ** 3)
            storage_ok = disk_gb > 0 and disk_gb <= free_gb
            storage_detail = f"Requested {disk_gb} GB; {free_gb} GB available on {parent}"
        except OSError as exc:
            storage_ok = False
            storage_detail = f"Cannot inspect storage: {exc}"

        vbox = shutil.which("VBoxManage")
        return [
            Check("VirtualBox CLI", vbox is not None, vbox or "VBoxManage not found"),
            Check("VM name", bool(vm.get("name")), vm.get("name", "missing")),
            Check("Memory", int(vm.get("memory_mb", 0)) >= 4096, f'{vm.get("memory_mb", 0)} MB configured'),
            Check("CPU count", int(vm.get("cpus", 0)) >= 2, f'{vm.get("cpus", 0)} configured'),
            Check("Virtual disk capacity", storage_ok, storage_detail),
            Check("Windows ISO", bool(iso and iso.is_file()), str(iso) if iso else "not configured"),
        ]

    def is_installed(self) -> bool:
        return False

    def is_active(self) -> bool:
        return False

    def install(self) -> ActionResult:
        blockers = [check for check in self.checks() if check.blocking and not check.ok]
        if blockers:
            return ActionResult(
                False,
                "\n".join([
                    'Cannot install "windows-11".',
                    *[f"• {check.name}: {check.detail}" for check in blockers],
                ]),
                self.checks(),
            )
        return ActionResult(False, "windows-11 installation is still a prototype and has not been implemented yet.", self.checks())

    def enable(self) -> ActionResult:
        return self.install()

    def disable(self) -> ActionResult:
        return ActionResult(True, '"windows-11" disable routine is not implemented yet.', self.checks(), False)
