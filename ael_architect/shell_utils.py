# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/shell_utils.py]
# :author        : fantomH
# :created       : 2024-09-08 16:10:31 UTC
# :updated       : 2024-09-08 16:10:36 UTC
# :description   : Shell utils utils.

import os
import re
import sqlite3

from config import AEL_DB
from database import table_shell_utils

def install_shell_util(shell_util_id):

    table_shell_utils()
    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM scripts WHERE id = ?', (shell_util_id,))
        row = cursor.fetchone()

        if row:
            column_names = [description[0] for description in cursor.description]

            util = dict(zip(column_names, row))

            aelcore = os.path.join(os.path.expanduser('~'), '.ael', '.aelcore')

            with open(aelcore, mode='r') as INPUT:
                data = INPUT.read()

                pattern = rf"\[ -f.*{util['filename']}.*{util['filename']}\n"
                match = re.search(pattern, data)
                if match and util['is_active']:
                    pass
                elif match and not util['is_active']:
                    new_data = re.sub(rf"{re.escape(match[0])}", '', data)
                    with open(aelcore, mode='w') as OUTPUT:
                        OUTPUT.write(new_data)
                elif not match and util['is_active']:
                    with open(aelcore, mode='a') as OUTPUT:
                        OUTPUT.write(f"[ -f ${{HOME}}/{util['filename']} ] && . ${{HOME}}/{util['filename']}\n")

                #[ -f ${HOME}/.ael/scripts/busy ] && . ${HOME}/.ael/scripts/busy
                # if util['is_active']:
                    # print(f'{util['name']} is active')
                    # pattern = rf"\[ -f.*{util['filename']}.*{util['filename']}\n"
                    # match = re.search(pattern, data)
                    # if match:
                        # print(match[0])
                # else:
                    # print(f'{util['name']} is NOT active')


if __name__ == "__main__":
    for x in range(0, 100):
        install_shell_util(x)
