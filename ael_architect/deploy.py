# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/deploy.py]
# :author        : fantomH
# :created       : 2024-09-27 14:00:44 UTC
# :updated       : 2024-09-27 14:00:48 UTC
# :description   : Deploy.

import re
import os
import sqlite3
import subprocess
# import tomllib

from config import AEL_DB
from packages import packages_table
from utils import get_linux_id

def install_packages(packages: list) -> None:

    def install(command):

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

    packages_table()

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
            file = cursor.fetchone()

            print(file)

            # :/Check if source exists.
            # if os.path.exists(file['src']):
                # print(file['name'], 'yes')
            # else:
                # print(file['name'], 'no')
            

if __name__ == '__main__':
    install_files(['dockerfiles--Dockerfile-kali'])
