# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/architect.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2024-12-11 11:28:21 UTC
# :description   : Main.

import argparse
import os
import subprocess
import tomllib

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

def deploy_ael_file(files_toml, file_id):
    with open(files_toml, 'rb') as _input:
        data = tomllib.load(_input)

        print(data["root--ael"])

def main():

    parser = argparse.ArgumentParser(description="AEL Architect.")

    parser.add_argument('--config', help="Path to custom ael.toml configuration file.")
    parser.add_argument('--system-wide', action="store_true", help="Install AEL system-wide. This will take over the system and affect all of its users.")

    args = parser.parse_args()

    if not args.system_wide:

        user_home = os.path.expanduser("~")
        src_files_repository = "https://github.com/alterEGO-Linux/ael-files.git"
        local_files_repository = os.path.join(user_home, ".local/share/ael-files")
        ael_directory = os.path.join(user_home, ".ael")

        # :Clone or pull source 
        check_local_git_repository(src_files_repository, local_files_repository)

        # :Make sure path ~/.ael/ exists.
        os.makedirs(ael_directory, exist_ok=True)

        if args.config:
            ael_config_file = args.config
        else:
            deploy_ael_file(os.path.join(local_files_repository, "files.toml"), "root--ael")
    else:
        print("System-wide take over not yet implemented!")

if __name__ == "__main__":
    main()
