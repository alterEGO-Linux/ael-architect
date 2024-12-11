# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/architect.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2024-09-25 12:09:40 UTC
# :description   : Main.

import argparse
import importlib.util
import os
import subprocess

from config import AEL_BUILD_DIRECTORY as default_build_dir
from files import files_table
from packages import packages_table
from sysconfig import run_sysconfig

def load_config(config_path):
    """Dynamically load a config file."""
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

def create_virtualbox_archlinux(build_dir, vm_name):
    # Get the absolute path of the shell script in the 'scripts' directory
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'virtualbox_archlinux.sh')

    if not os.path.exists(script_path):
        print(f"Error: {script_path} does not exist.")
        return

    print(f"Running {script_path} with VM name: {vm_name}")
    result = subprocess.run([script_path], env={"BUILD_DIR": build_dir, "VM_NAME": vm_name}, check=True)
    
    if result.returncode == 0:
        print(f"VM {vm_name} creation succeeded.")
    else:
        print(f"VM {vm_name} creation failed.")

def main():
    parser = argparse.ArgumentParser(description="AEL Architect.")

    parser.add_argument('--config', help="Path to custom config.py.")

    parser.add_argument('--virtualbox', 
                        choices=['archlinux'],
                        help="Specify Linux distro to install (e.g., archlinux)")
    parser.add_argument('--name',
                        help="Name of the Virtual Machine (required with --virtualbox)")
    args = parser.parse_args()

    if args.virtualbox:
        if not args.name:
            parser.error("--name is required when --virtualbox is specified")
        else:
            if args.config:
                config = load_config(args.config)
                build_dir = getattr(config, 'AEL_BUILD_DIRECTORY', default_build_dir)
                create_virtualbox_archlinux(build_dir, args.name)
            else:
                build_dir = default_build_dir
                create_virtualbox_archlinux(build_dir, args.name)
        # print(f"[+] Starting System Configuration...")
        # print(f"[-] Updating files tables...")
        # files_table()
        # print(f"[-] Updating packages tables...")
        # packages_table()
        # run_sysconfig()

if __name__ == "__main__":
    main()
