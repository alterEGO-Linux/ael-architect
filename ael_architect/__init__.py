# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/__init__.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2024-12-11 11:47:30 UTC
# :description   : Main.

import argparse
import os
import subprocess

def check_local_git_repository(remote_url, local_path):

    if os.path.exists(local_path) and os.path.isdir(os.path.join(local_path, ".git")):
        print(f"Repository already exists at {local_path}. Pulling the latest changes...")
        try:
            subprocess.run(["git", "-C", local_path, "pull"], check=True)
            print("Repository updated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error pulling the repository: {e}")
    else:
        print(f"Repository does not exist at {local_path}. Cloning...")
        try:
            subprocess.run(["git", "clone", remote_url, local_path], check=True)
            print("Repository cloned successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning the repository: {e}")

def main():

    parser = argparse.ArgumentParser(description="AEL Architect.")

    parser.add_argument('--config', help="Path to custom ael.toml configuration file.")
    parser.add_argument('--system-wide', action="store_true", help="Install AEL system-wide. This will take over the system and affect all of its users.")

    args = parser.parse_args()

    if not args.system_wide:
        remote_url = "https://github.com/alterEGO-Linux/ael-files.git"
        local_path = os.path.expanduser("~/.local/share/ael-files")
        check_local_git_repository(remote_url, local_path)
    else:
        print("System-wide take over not yet implemented!")

if __name__ == "__main__":
    main()
