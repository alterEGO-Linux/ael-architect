## ----------------------------------------------------------------------- INFO
## [AELarchitect/architect.py]
## author        : fantomH @alerEGO Linux
## created       : 2023-11-20 00:23:25 UTC
## updated       : 2024-02-15 15:24:29 UTC
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
from config import (AELFILES_GIT,
                    AELFILES_LOCAL,
                    AELFILES_CONFIG,
                    ARCHITECT_CONFIG,
                    USER)

## Checking privileges.
if os.getenv('USER') == 'root':
    _user = 'root_user'
else:
    _user = 'normal_user'

## -------------------- [ UTILS ] 

# def menu(opt):

    # opt = ''.join([f"{o}\n" for o in opt]).encode('UTF-8')

    # menu = subprocess.run(['fzf', 
                           # "--prompt=AEL Architect ❯ ",
                           # "--header= ",
                           # "--no-hscroll",
                           # "--reverse",
                           # "-i",
                           # "--exact",
                           # "--tiebreak=begin",
                           # "--no-info",
                           # "--pointer=•",
                           # ], input=opt, stdout=subprocess.PIPE)

    # selection = menu.stdout.decode('UTF-8')

    # return selection.strip()

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

def get_files():
    if os.path.isdir(AELFILES_LOCAL):
        message('action', f'Found {AELFILES_LOCAL}')
        message('results', f'Updating AEL files...')
        execute(f"git pull", cwd=AELFILES_LOCAL)
    else:
        message('action', f"Downloading AEL files...")
        execute(f"git clone {AELFILES_GIT} {AELFILES_LOCAL}")

## -------------------- [ FILES ] 

def copy_files():

    with open(AELFILES_CONFIG, 'rb') as _input:
        data = tomllib.load(_input)

        ## Convert dict of dict to namedtuple
        AELFiles = namedtuple('AELFiles', ['filename', 'category', 'src', 'dst', 'description', 'modes', 'is_symlink', 'create_bkp'])
        files = [AELFiles(**values) for values in data['file'].values()]

        for f in files:
            if f.src.startswith('AELFILES_LOCAL'):
                src = os.path.join(AELFILES_LOCAL,  f.src.replace('AELFILES_LOCAL/', ''), f.filename)
            else:
                src = os.path.join(f.src, f.filename)

            ## Checks if dst directory exists.
            dst_directory = os.path.dirname(f.dst)
            if not os.path.exists(dst_directory):
                os.makedirs(dst_directory)

            ## Checks if exists.
            if os.path.exists(f.dst):
                ## (* BACKUP *)
                if f.create_bkp == True:
                    os.rename(f.dst, f.dst + ".aelbkup")
                else:
                    os.remove(f.dst)
            else:
                ## Remove broken symlinks.
                if os.path.islink(f.dst):
                    os.remove(f.dst)

            ## (* SYMLINK *)
            if f.is_symlink == True:
                message('results', f'Symlink {f.dst}')
                os.symlink(src, f.dst)
            ## (* COPY *)
            else:
                message('results', f'Copying {f.dst}')
                shutil.copy2(src, f.dst)

            ## (* HOME *)
            if "/skel/" in f.dst:
                dst = f.dst.replace('/etc/skel', '/home/' + USER)

                ## Checks if dst directory exists.
                dst_directory = os.path.dirname(dst)
                if not os.path.exists(dst_directory):
                    os.makedirs(dst_directory)
                    shutil.chown(dst_directory, USER, 'users')

                ## (* BACKUP *)
                if os.path.exists(dst):
                    os.rename(dst, dst + ".aelbkup")
                else:
                    ## Remove broken symlinks.
                    if os.path.islink(dst):
                        os.remove(dst)

                message('results', f'Copying {dst}')
                shutil.copy2(src, dst)
                shutil.chown(dst, USER, 'users')
class Menu:

    def fzf(self, opt):

        opt = ''.join([f"{o}\n" for o in opt]).encode('UTF-8')

        menu = subprocess.run(['fzf', 
                            "--prompt=AEL Architect ❯ ",
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
            execute(f"vim {ARCHITECT_CONFIG}")
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
