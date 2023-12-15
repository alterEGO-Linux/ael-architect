## ----------------------------------------------------------------------- INFO
## [AELarchitect/architect.py]
## author        : fantomH @alerEGO Linux
## created       : 2023-11-20 00:23:25 UTC
## updated       : 2023-12-07 19:51:37 UTC
## description   : Installer and Updater.

import argparse
from collections import namedtuple
import os
import shlex
import shutil
import subprocess
import sys
import time
import tomllib

import config

## Checking privileges.
if os.getenv('USER') == 'root':
    _user = 'root_user'
else:
    _user = 'normal_user'

## -------------------- [ UTILS ] 

def menu(opt):

    opt = ''.join([f"{o}\n" for o in opt]).encode('UTF-8')

    menu = subprocess.run(['fzf', 
                           "--prompt=LAUNCH ❯ ",
                           "--header= ",
                           "--no-hscroll",
                           "--reverse",
                           "-i",
                           "--exact",
                           "--tiebreak=begin",
                           "--no-info",
                           "--pointer=•",
                           ], input=opt, stdout=subprocess.PIPE)

    selection = menu.stdout.decode('UTF-8')

    return selection.strip()

## ---------- (* messages *) 
def message(msg_type, msg, wait=0):

    foreground_blue = '\033[34m'
    foreground_green = '\033[32m'
    foreground_red = '\033[31m'
    format_bold = '\033[1m'
    format_reset = '\033[00m'

    if msg_type == "action":
        print(f"{foreground_green}[*]{format_reset} {format_bold}{msg}{format_reset}")
    elif msg_type == "result":
        print(f"{foreground_blue}[-]{format_reset} {format_bold}{msg}{format_reset}")
    elif msg_type in ["warning", "error"]:
        print(f"{foreground_red}[!]{format_reset} {format_bold}{msg}{format_reset}")
    else:
        print(f"    {format_bold}{msg}{format_reset}")

    time.sleep(wait)

## ---------- (* execute *)
def execute(cmd, cwd=None, shell=False, text=True, input=None):

    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)
    if input:
        input = input.encode()
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, input=input)

    CommandResults = namedtuple('CommandResults', ['returncode'])
    return CommandResults(cmd_run.returncode)

## -------------------- [ GIT ]

FILES_URL = 'https://github.com/alterEGO-Linux/ael-files.git'
FILES_PATH = '/usr/share/ael/cache/files'

def get_files():
    if os.path.isdir(FILES_PATH):
        message('action', f'Found {FILES_PATH}')
        message('results', f'Updating AEL files...')
        execute(f"git pull", cwd=FILES_PATH)
    else:
        message('action', f"Downloading AEL files...")
        execute(f"git clone {FILES_URL} {FILES_PATH}")

## -------------------- [ FILES ] 

def copy_files():
    FILES_CONFIG = os.path.join(FILES_PATH, 'usr', 'share', 'ael', 'files.toml')

    with open(FILES_CONFIG, 'rb') as _input:
        data = tomllib.load(_input)

        ## Convert dict of dict to namedtuple
        AELFiles = namedtuple('AELFiles', ['filename', 'category', 'src', 'dst', 'description', 'mode', 'is_symlink', 'create_bkp'])
        files_list = [AELFiles(**values) for values in data['file'].values()]

        for f in files_list:
            if f.src == 'FILESGIT':
                _src = FILES_PATH + os.path.join(f.dst, f.filename)
            else:
                _src = os.path.join(f.src, f.filename)

            _dst = os.path.join(f.dst, f.filename)

            os.makedirs(f.dst, exist_ok = True)
            if f.create_bkp == True:
                pass
            else:
                if os.path.exists(_dst):
                    os.remove(_dst)
                    message('results', f'Copying {_dst}...')
                    shutil.copy2(_src, _dst)
                else:
                    message('results', f'Copying {_dst}...')
                    shutil.copy2(_src, _dst)

class Menu:

    def fzf(self, opt):

        opt = ''.join([f"{o}\n" for o in opt]).encode('UTF-8')

        menu = subprocess.run(['fzf', 
                            "--prompt=LAUNCH ❯ ",
                            "--header= ",
                            "--no-hscroll",
                            "--reverse",
                            "-i",
                            "--exact",
                            "--tiebreak=begin",
                            "--no-info",
                            "--pointer=•",
                            ], input=opt, stdout=subprocess.PIPE)

        selection = menu.stdout.decode('UTF-8')

        return selection.strip()

    def main_menu(self):
        main_items = ["Review installation config",
                      "Update system",
                      "Exit"]

        selection = self.fzf(main_items)

        if selection == "Review installation config":
            execute(f"vim {config.CONFIG}")
            # what = input(f"What's your name: ")
            # main_items.append(what)
            # selection = self.fzf(main_items)
            self.main_menu()

        elif selection == "Update system":
            get_files()
            copy_files()
            self.main_menu()
            
        elif selection == 'Exit':
            sys.exit(0)
        else:
            return selection

def main():

    menu = Menu()

    menu.main_menu()

    # if menu.main_menu() == "Review installation config":
        # execute(f"vim {config.CONFIG}")
        # menu.main_menu()


    t_menu = menu(['YES', 'NO'])

    if t_menu == 'YES':
        sys.exit()


if __name__ == '__main__':
    main()

    # get_files()
    # copy_files()

    # s1 = menu(['1', '2', '3'])
    # execute(f"echo 'hello'")
    # print(s1 + "l")
    # if s1 == '1':
        # print(type(s1))
        # s2 = menu(['yes', 'no'])
        # print(s2)

# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
