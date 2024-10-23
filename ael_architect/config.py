# :----------------------------------------------------------------------- INFO
# :ael-rchitect/ael_architect/config.py]
# :author        : fantomH @alterEGO Linux
# :created       : 2023-12-14 11:37:06 UTC
# :updated       : 2024-10-23 10:29:06 UTC
# :description   : General config for ael-architect.

import os

# :---/ architect.db /---:

AEL_DB = os.path.join(os.path.expanduser('~'), '.ael', 'ael.db')
AEL_BUILD_DIRECTORY = os.path.join(os.path.expanduser('~'), '.cache', '.build')

## PATHS
AELFILES_GIT = 'https://github.com/alterEGO-Linux/ael-files.git'
AELFILES_LOCAL = '/usr/share/ael/cache/files'
AELFILES_CONFIG = os.path.join(AELFILES_LOCAL, 'usr', 'share', 'ael', 'files.toml')
ARCHITECT_CONFIG = '/home/ghost/main/ael-architect/AELarchitect/config.py'

# :---------- [ GENERAL CONFIG ]
TIMEZONE = 'America/New_York'
HOSTNAME = 'alterEGO'
ROOT_PASSWD = 'toor'
USER = 'ghost'
USER_PASSWD = 'password1'
