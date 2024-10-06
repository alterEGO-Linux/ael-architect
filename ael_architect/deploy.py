# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/deploy.py]
# :author        : fantomH
# :created       : 2024-09-27 14:00:44 UTC
# :updated       : 2024-09-27 14:00:48 UTC
# :description   : Deploy.

import re
import os
import shutil
import sqlite3
import subprocess
# import tomllib

from config import AEL_DB
from packages import packages_table
from files import files_table
from utils import get_linux_id
from utils import md5sum

def install_packages(packages: list) -> None:

    def install(command: list) -> None:

        try:
            result = subprocess.run(
                        command,
                        check=True,
                        text=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        )
            print("Packages installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while installing packages: {e}")

    # :/Verify which linux flavor.
    linux_id = get_linux_id()

    # :/Distro -> Arch Linux    
    if linux_id in ['arch', 'ael', 'manjaro']:
        for package in packages:
            with sqlite3.connect(AEL_DB) as conn:
                cursor = conn.cursor()

                cursor.execute('SELECT archlinux FROM packages WHERE name = ?', (package,))
                repo = cursor.fetchone()

                # :/pacman
                if repo[0].startswith(('core', 'extra')):
                    package = repo[0].split('/')[1]
                    package = re.sub(r'\(.*?\)', '', package)
                    command = ['sudo', 'pacman', '-S', '--noconfirm', '--needed', package]
                    install(command)

                # :/paru
                if repo[0].startswith(('aur')):
                    package = repo[0].split('/')[1]
                    package = re.sub(r'\(.*?\)', '', package)
                    command = ['paru', '-S', '--noconfirm', '--needed', package]
                    install(command)

def install_files(files: list) -> None:

    for file in files:

        with sqlite3.connect(AEL_DB) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM files WHERE name = ?', (file,))
            row = cursor.fetchone()
            if row:
                column_names = [description[0] for description in cursor.description]
                file = dict(zip(column_names, row))

        # :/Making sure directories exists.
        directory = os.path.dirname(file['dst'])
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        # :/Update file if necessary
        if os.path.exists(file['dst']):
            if file['dst'] != file['src'] and md5sum(file['dst']) != md5sum(file['src']):
                if file['is_symlink']:
                    subprocess.run(['sudo', 'ln', '-sf', file['src'], file['dst']], check=True)
                else:
                    if file['create_bkp']:
                        if not os.path.islink(file['dst']):
                            shutil.copy2(file[dst], file[dst] + ".aelbkp")
                    subprocess.run(['sudo', 'cp', file['src'], file['dst']], check=True)
        # :/Create file.
        else:
            if file['is_symlink']:
                subprocess.run(['sudo', 'ln', '-sf', file['src'], file['dst']], check=True)
            else:
                subprocess.run(['sudo', 'cp', file['src'], file['dst']], check=True)

if __name__ == '__main__':
    install_files(['shellutils--cheat'])
