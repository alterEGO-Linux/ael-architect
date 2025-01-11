# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/architect.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2025-01-09 10:49:56 UTC
# :description   : Main.

import argparse
import hashlib
import os
from pathlib import Path
import shutil
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

def get_md5(f):

    hash_md5 = hashlib.md5()
    with open(f, "rb") as _input:
        for chunk in iter(lambda: _input.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def deploy_ael_file(file_id):

    AEL_FILES_TOML = os.path.join(LOCAL_FILES_REPOSITORY, 'files.toml')
    with open(AEL_FILES_TOML, 'rb') as _input:
        data = tomllib.load(_input)

    for path in ['src', 'dst']:
        if data[file_id][path]:
            data[file_id][path] = data[file_id][path].replace('USERHOME', USERHOME).replace('USRSHARE', USRSHARE)

    src = Path(data[file_id]['src'])
    dst = Path(data[file_id]['dst'])
    is_symlink = data[file_id]['is_symlink']
    create_bkp = data[file_id]['create_bkp']

    # :Create parent directories.
    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        if dst.is_symlink():
            if is_symlink:
                # Update symlink if it points to a different source
                if dst.resolve() != src:
                    print(f"Updating symlink: {dst} -> {src}")
                    dst.unlink()
                    dst.symlink_to(src)
            else:
                # Replace symlink with a regular file
                print(f"Replacing symlink with file: {dst}")
                dst.unlink()
                shutil.copy2(src, dst)
        else:
            if is_symlink:
                # Replace regular file with a symlink
                print(f"Replacing file with symlink: {dst} -> {src}")
                if create_bkp:
                    backup = dst.with_suffix(dst.suffix + ".bkp")
                    print(f"Creating backup: {backup}")
                    shutil.copy2(dst, backup)
                dst.unlink()
                dst.symlink_to(src)
            else:
                # Replace the file only if contents differ
                if get_md5(dst) != get_md5(src):
                    print(f"Updating file: {dst}")
                    if create_bkp:
                        backup = dst.with_suffix(dst.suffix + ".bkp")
                        print(f"Creating backup: {backup}")
                        shutil.copy2(dst, backup)
                    shutil.copy2(src, dst)
    else:
        # Destination does not exist
        if is_symlink:
            print(f"Creating symlink: {dst} -> {src}")
            dst.symlink_to(src)
        else:
            print(f"Copying file: {src} -> {dst}")
            shutil.copy2(src, dst)


def main():

    parser = argparse.ArgumentParser(description="AEL Architect.")

    parser.add_argument('--config', help="Path to custom ael.toml configuration file.")
    parser.add_argument('--system-wide', action="store_true", help="Install AEL system-wide. This will take over the system and affect all of its users.")

    args = parser.parse_args()

    if not args.system_wide:

        SRC_FILES_REPOSITORY = "https://github.com/alterEGO-Linux/ael-files.git"

        global USERHOME
        USERHOME = os.path.expanduser("~")

        global USRSHARE
        USRSHARE = os.path.join(USERHOME, '.local/share')
        
        global LOCAL_FILES_REPOSITORY
        LOCAL_FILES_REPOSITORY = os.path.join(USRSHARE, "ael-files")

        AEL_DIRECTORY = os.path.join(USERHOME, ".ael")

        # :Clone or pull source 
        check_local_git_repository(SRC_FILES_REPOSITORY, LOCAL_FILES_REPOSITORY)

        # :Make sure path ~/.ael/ exists.
        os.makedirs(AEL_DIRECTORY, exist_ok=True)

        if args.config:
            ael_config_file = args.config
        else:
            deploy_ael_file("root--ael")
    else:
        print("System-wide take over not yet implemented!")

if __name__ == "__main__":
    main()
