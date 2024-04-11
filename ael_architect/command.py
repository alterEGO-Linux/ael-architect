#! /usr/bin/env python
# :----------------------------------------------------------------------- INFO
# :[Snake-Vault/snake_vault/command.py]
# :author        : fantomH @alterEGO Linux
# :created       : 2023-12-08 11:52:32 UTC
# :updated       : 2024-04-10 19:58:50 UTC
# :description   : Commands utils

from collections import namedtuple
import shlex
import subprocess

def execute(cmd, cwd=None, shell=False, text=True, input=None, interact=False):

    """execute() - A custom function to run subprocess

    # :module : Snake-Vault/snake_vault/command.py
    # :version: 2024-04-07 13:56:33 UTC

    Arguments:
        cmd: (str) Command to be executed.
             If the command includes variables or input, use f-string.
             Example:
                hello = "Hello world"
                execute(f"echo {hello}")
             By default, the string will be split into a list, using shlex.split
             to satisfy subprocess function.
             If the command includes pipes, or other shell characters, set the 
             argument `shell` to True. See shell.
        cwd: (str, default: None) Current working directory.
             If you need to run the command in a particular directory.
        shell: (bool, default: False) Run command as in the terminal.
             Set `shell` to True if you have any shell reserved characters,
             such as pipes or redirections.
             Example:
                execute(f"find / -iname *password* 2>/dev/null | grep '/usr/share'", shell=True)
        text: (bool, default: True) stdout, stderr as string, not bytes.
        input: (str, default: None) Takes a string the command need to injest.
             Input will be encoded to satisfy subprocess.
        interact: (bool, default: False) In order to interact with a subprocess,
             capture_output must be disabled. Thus, you cannot capture the 
             stdout and stderr, and run the subprocess with manual intervention
             at the same time.
    """

    # :Shell
    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)

    # :Standard input.
    if input:
        input = input.encode()

    # :Interact
    if interact:
        capture_output = False
    else:
        capture_output = True
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, input=input, capture_output=capture_output)

    CommandResults = namedtuple('CommandResults', ['returncode',
                                                   'stdout',
                                                   'stderr',
                                                   'args',
                                                   'cwd',
                                                   'input'])

    result = CommandResults(cmd_run.returncode, cmd_run.stdout, cmd_run.stderr, cmd_run.args, cwd, input)
    return result

if __name__ == "__main__":

    pass

# :------------------------------------------------------------- FIN ¯\_(ツ)_/¯
