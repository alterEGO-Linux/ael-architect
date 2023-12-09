#! /usr/bin/env python
## ----------------------------------------------------------------------- INFO
## [AELarchitect/packages.py]
## author        : fantomH @alterEGO Linux
## created       : 2023-12-08 11:12:16 UTC
## updated       : 2023-12-08 11:12:16 UTC
## description   : Generates packages lists and stuff.

import sqlite3 as sql

from command import execute

DB = '/home/ghost/main/ael-files/usr/share/dev/ael-dev.db'

def packages_list(mode='hacker'):

    con = sql.connect(DB)
    cur = con.cursor()

    q = f"""SELECT package FROM packages WHERE mode LIKE '%{mode}%'"""
    cur.execute(q)
    records = cur.fetchall()

    return [p[0] for p in records]

    con.close

def package_info(package):
    pkg_info = execute(f"paru -Si {package}", capture_output=True).stdout.decode("UTF-8").split("\n")

    pkg_Ql = execute(f"paru -Qlq {package}", capture_output=True).stdout.decode("UTF-8").split("\n")

    # pkgs_info = []

    package_info = {}
    for line in pkg_info:
        package_info["package"] = package
        if line.startswith("Repository"):
            package_info["repository"] = line.split(":")[1].strip()
        if line.startswith("Description"):
            package_info["description"] = line.split(":")[1].strip() + "."
        if line.startswith("URL"):
            package_info["url"] = line.split(": ")[1]

    if package_info.get('repository') is None:
        print(f"{package_info.get('package')}")
    else:
        pass

    package_Ql_bin = []
    for line in pkg_Ql:
        if "/usr/bin/" in line and not line.endswith("/"):
            package_Ql_bin.append(line)
        else:
            pass
            # print(line)

    package_info["Ql_bin"] = package_Ql_bin
    
    return ' '

def main():

    pkgs = packages_list(mode='hacker')

    for p in pkgs:
        package_info(p)

if __name__ == "__main__":
    main()

# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
