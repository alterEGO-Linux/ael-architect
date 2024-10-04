# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/utils.py]
# :author        : fantomH
# :created       : 2024-09-27 14:00:44 UTC
# :updated       : 2024-09-28 18:49:31 UTC
# :description   : Utils.

import hashlib
# import re
# import os
# import sqlite3
# import subprocess
# import tomllib

# from config import AEL_DB
# from packages import packages_table

def get_linux_id() -> str:
    with open("/etc/os-release", "r") as file:
        for line in file:
            if line.startswith("ID="):
                return line.strip().split('=')[1]

def md5sum(filepath):
    md5_hash = hashlib.md5()

    with open(filepath, "rb") as INPUT:
        for chunk in iter(lambda: INPUT.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()

if __name__ == '__main__':
    l = get_linux_id()
    print(l)

