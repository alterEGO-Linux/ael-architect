#! /usr/bin/env python
## ----------------------------------------------------------------------- INFO
## [AELarchitect/packages.py]
## author        : fantomH @alterEGO Linux
## created       : 2023-12-08 11:12:16 UTC
## updated       : 2024-01-16 12:39:23 UTC
## description   : Generates packages lists and stuff.

from datetime import (datetime,
                      timezone)
import os
import sqlite3 as sql
import tomllib

from command import execute

DB = '/home/ghost/main/ael-files/usr/share/dev/ael-dev.db'

def packages_list(modes=['hyprland', 'i3wm', 'pip']):

    con = sql.connect(DB)
    cur = con.cursor()

    q = f"""SELECT package, mode FROM packages"""
    cur.execute(q)
    records = cur.fetchall()

    records = [(p[0], p[1].split()) for p in records]

    packages = []
    for p in records:
        if set(modes).intersection(p[1]):
            packages.append(p[0])

    return packages

    con.close

def package_info(package):

    package_info = {}

    pkg_Si = execute(f"paru -Si {package}", capture_output=True).stdout.decode("UTF-8").split("\n")
    for line in pkg_Si:
        ## Package name.
        package_info["name"] = package
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

    package_info["bin"] = package_Ql_bin
    package_info["Ql_desktop"] = package_Ql_desktop
    package_info["Ql_man"] = package_Ql_man
    package_info["Ql_info"] = package_Ql_info

    ## (* modes *)
    con = sql.connect(DB)
    cur = con.cursor()
    q = f"""SELECT mode FROM packages WHERE package == '{package}'"""
    cur.execute(q)
    modes = cur.fetchone()

    package_info["modes"] = [mode for mode in modes]
    con.close

    return package_info

def generate_packagestoml(modes=['i3wm', 'hyprland', 'pip']):

    pkgs = sorted(packages_list(modes=modes))

    packagestoml = "/home/ghost/main/ael-files/usr/share/ael/packages.toml"

    with open(packagestoml, mode='w') as file_out:
        file_out.write(f"""\
## ----------------------------------------------------------------------- INFO
## [/usr/share/ael/packages.toml]
## author        : fantomH @alterEGO Linux
## created       : 2023-10-22 15:06:13 UTC
## updated       : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}
## description   : Packages list.

""")

        for pkg in pkgs:
            pkg_info = package_info(pkg)
            file_out.write(f"""\
[{pkg_info.get('name')}]
repository      = "{pkg_info.get('repository')}"
url             = "{pkg_info.get('url')}"
description     = "{pkg_info.get('description')}"
modes           = {pkg_info.get('modes')}

""")

        file_out.write(f"""\
# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
""")

def packages_diff():

    PACKAGES = os.path.join('/', 'home', 'ghost', 'main', 'ael-files', 'usr', 'share', 'ael', 'packages.toml')

    with open(PACKAGES, 'rb') as _input:
        data = tomllib.load(_input)

        from_PACKAGES = [x for x in data.keys()]
    
    locally = execute(f"paru -Qeq", capture_output=True).stdout.decode("UTF-8").split("\n")

    print(set(from_PACKAGES).difference(locally))

def main():

    ## packages_list(mode='hyprland')
    # for p in packages_list(modes=['hyprland']):
        # print(p)

    ## package_info(package)
    # for p in packages_list(modes=['hyprland']):
        # print(package_info(p))

    ## (* Generate packages.toml *)
    # generate_packagestoml()

    ## (* Packages diff *)
    packages_diff()

if __name__ == "__main__":
    main()

# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
