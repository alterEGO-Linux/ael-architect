#! /usr/bin/env python
## ----------------------------------------------------------------------- INFO
## [AELarchitect/packages.py]
## author        : fantomH @alterEGO Linux
## created       : 2023-12-08 11:12:16 UTC
## updated       : 2024-01-16 12:39:23 UTC
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

    pkg_Si = execute(f"paru -Si {package}", capture_output=True).stdout.decode("UTF-8").split("\n")
    package_info = {}
    for line in pkg_Si:
        ## Package name.
        package_info["package"] = package
        ## Package repository.
        if line.startswith("Repository"):
            package_info["repository"] = line.split(":")[1].strip()
        ## Package description.
        if line.startswith("Description"):
            package_info["description"] = line.split(":")[1].strip() + "."
        ## Package URL
        if line.startswith("URL"):
            package_info["url"] = line.split(": ")[1]
        if line.startswith("AUR URL"):
            package_info["aur_url"] = line.split(": ")[1]

    if package_info.get('repository') is None:
        pass
        # print(f"{package_info.get('package')}")
    else:
        pass

    pkg_Ql = execute(f"paru -Qlq {package}", capture_output=True).stdout.decode("UTF-8").split("\n")
    # for line in pkg_Ql:
        # print(line)
        # if line.endswith(".md"):
            # print(line)
            # execute(f"glow {line}")

    package_Ql_bin = []
    package_Ql_desktop = []
    package_Ql_man = []
    package_Ql_info = []
    for line in pkg_Ql:
        ## Package executables.
        if "/usr/bin/" in line and not line.endswith("/"):
            package_Ql_bin.append(line)
        ## Package desktop.
        if line.endswith(".desktop"):
            package_Ql_desktop.append(line)
        ## Package man.
        if "/man/" in line and line.endswith(".gz"):
            _man = line.split("/")[-1].split(".")
            _man = f"{'.'.join(_man[0:-2])}({_man[-2]})"
            package_Ql_man.append(_man)
        ## Info.
        if "/info/" in line and line.endswith(".gz"):
            _info = line.split("/")[-1].split(".")
            _info = f"{'.'.join(_info[0:-2])}"
            package_Ql_info.append(_info)
        ## Is Python?
        if "/usr/lib/python" in line:
            package_info["is_python"] = True
            break
        else:
            package_info["is_python"] = False
        ## Documentation.
        if ("/doc/") in line:
            package_info["has_docs"] = True
        else:
            package_info["has_docs"] = False

    package_info["Ql_bin"] = package_Ql_bin
    package_info["Ql_desktop"] = package_Ql_desktop
    package_info["Ql_man"] = package_Ql_man
    package_info["Ql_info"] = package_Ql_info

    return package_info

def main():

    pkgs = packages_list(mode='hacker-hyprland')

    for p in pkgs:
        print(package_info(p))

if __name__ == "__main__":
    main()

# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
