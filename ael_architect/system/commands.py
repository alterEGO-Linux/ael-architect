from __future__ import annotations
import shutil

def command_path(command: str) -> str | None:
    return shutil.which(command)

def command_exists(command: str) -> bool:
    return command_path(command) is not None

def commands_exist(commands: list[str]) -> bool:
    return all(command_exists(command) for command in commands)

def missing_commands(commands: list[str]) -> list[str]:
    return [command for command in commands if not command_exists(command)]
