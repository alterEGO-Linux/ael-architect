#! /usr/bin/env python
## ----------------------------------------------------------------------- INFO
## [command.py]
## author        : fantomH @alterEGO Linux
## created       : 2023-12-08 11:52:32 UTC
## updated       : 2023-12-08 11:52:32 UTC
## description   : Commands utils

from collections import namedtuple
import shlex
import subprocess

def execute(cmd, cwd=None, shell=False, capture_output=False, text=True, input=None):

    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)
    if input:
        input = input.encode()
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, capture_output=capture_output, input=input)

    return cmd_run
    # CommandResults = namedtuple('CommandResults', ['returncode'])
    # return CommandResults(cmd_run.returncode)

# vim: foldmethod=marker
## ------------------------------------------------------------- FIN ¯\_(ツ)_/¯
