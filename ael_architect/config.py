# :----------------------------------------------------------------------- INFO
# :ael_architect/config.py]
# :author        : fantomH @alterEGO Linux
# :created       : 2023-12-14 11:37:06 UTC
# :updated       : 2024-04-15 11:08:23 UTC
# :description   : General config for AELarchitect

import os

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

# :------------------------------------------------------------- FIN ¯\_(ツ)_/¯
