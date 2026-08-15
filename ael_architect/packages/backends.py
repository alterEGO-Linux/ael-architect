from __future__ import annotations
from pathlib import Path
import subprocess
from ael_architect.addons.base import ActionResult
from ael_architect.system.commands import command_path
from .models import PackageSpec

class PackageBackend:
    def run(self, command: list[str], *, sudo: bool=False, cwd: Path|None=None) -> ActionResult:
        if sudo:
            command = ["sudo", *command]
        try:
            result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
        except OSError as exc:
            return ActionResult(success=False, changed=False, message=str(exc))
        if result.returncode != 0:
            return ActionResult(success=False, changed=False, message=result.stderr.strip() or result.stdout.strip() or "Command failed.")
        return ActionResult(success=True, changed=True, message=result.stdout.strip() or "Installation completed.")

class PacmanBackend(PackageBackend):
    def install(self, spec, settings):
        pacman = command_path("pacman")
        if not pacman:
            return ActionResult(success=False, message="pacman was not found.")
        return self.run([pacman,"-S","--needed","--noconfirm",spec.package], sudo=True)

class AurBackend(PackageBackend):
    def install(self, spec, settings):
        helper_name = settings.get("aur_helper", "paru")
        helper = command_path(helper_name)
        if not helper:
            return ActionResult(success=False, message=f'AUR helper "{helper_name}" is not installed.')
        return self.run([helper,"-S","--needed","--noconfirm",spec.package])

class SnapBackend(PackageBackend):
    def install(self, spec, settings):
        snap = command_path("snap")
        if not snap:
            return ActionResult(success=False, message="snap is not installed.")
        return self.run([snap,"install",spec.package], sudo=True)

class FlatpakBackend(PackageBackend):
    def install(self, spec, settings):
        flatpak = command_path("flatpak")
        if not flatpak:
            return ActionResult(success=False, message="flatpak is not installed.")
        remote = spec.remote or "flathub"
        return self.run([flatpak,"install","--noninteractive","-y",remote,spec.package])

class GitBackend(PackageBackend):
    def install(self, spec, settings):
        git = command_path("git")
        if not git:
            return ActionResult(success=False, message="git is not installed.")
        if not spec.url:
            return ActionResult(success=False, message=f'"{spec.key}" does not define a Git URL.')
        root = Path(settings.get("git_root", "~/.cache/ael-architect/git")).expanduser()
        root.mkdir(parents=True, exist_ok=True)
        repository = root/spec.key
        if repository.is_dir():
            result = self.run([git,"pull","--ff-only"], cwd=repository)
        else:
            command=[git,"clone"]
            if spec.branch: command += ["--branch",spec.branch]
            command += [spec.url,str(repository)]
            result = self.run(command)
        if not result.success: return result
        if spec.install in (None,"clone"):
            return ActionResult(success=True, changed=True, message=f'Cloned "{spec.name}" to {repository}.')
        if spec.install == "make":
            make = command_path("make")
            if not make:
                return ActionResult(success=False, message="make is not installed.")
            result=self.run([make], cwd=repository)
            if not result.success: return result
            return self.run([make,"install"], cwd=repository, sudo=True)
        return ActionResult(success=False, message=f"Unsupported Git install method: {spec.install}")
