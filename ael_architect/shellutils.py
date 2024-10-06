# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/shellutils.py]
# :author        : fantomH
# :created       : 2024-09-07 02:03:22 UTC
# :updated       : 2024-09-08 14:16:01 UTC
# :description   : database.

import re
import os
import sqlite3

from config import AEL_DB
from deploy import install_files
from deploy import install_packages
from files import files_table
from packages import packages_table


def shellutils_to_listdicts():

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM files WHERE name LIKE 'shellutils%'")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        SHELLUTILS = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            row_dict['name'] = row_dict['name'].replace('shellutils--', '', 1)
            SHELLUTILS.append(row_dict)

        SHELLUTILS.sort(key=lambda x: x['name'])

        return SHELLUTILS

def shellutils_toggle(shellutil_id: str) -> None:

    """
    Used by sysconfig.py to activate/deactivate a Shell Util.
    """

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT is_active FROM files WHERE id = ?', (shellutil_id,))
        SHELLUTIL = cursor.fetchone()

        if SHELLUTIL:
            current_state = SHELLUTIL[0]
            new_state = 0 if current_state == 1 else 1
            cursor.execute('''
                UPDATE files
                SET is_active = ?
                WHERE id = ?
            ''',
            (new_state, shellutil_id))

        conn.commit()

        shellutil_update(shellutil_id)

        # :/Write to .aelcore.
        shellutil_to_aelcore(shellutil_id)

def shellutil_to_aelcore(shellutil_id: str) -> None:

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM files WHERE id = ?', (shellutil_id,))
        row = cursor.fetchone()

        if row:
            column_names = [description[0] for description in cursor.description]

            SHELLUTIL = dict(zip(column_names, row))

            AELCORE = os.path.join(os.path.expanduser('~'), '.ael', '.aelcore')

            with open(AELCORE, mode='r') as INPUT:
                data = INPUT.read()

                pattern = rf"\[ -f.*{SHELLUTIL['dst']}.*{SHELLUTIL['dst']}\n"
                match = re.search(pattern, data)
                if match and SHELLUTIL['is_active']:
                    pass
                elif match and not SHELLUTIL['is_active']:
                    new_data = re.sub(rf"{re.escape(match[0])}", '', data)
                    with open(AELCORE, mode='w') as OUTPUT:
                        OUTPUT.write(new_data)
                elif not match and SHELLUTIL['is_active']:
                    with open(AELCORE, mode='a') as OUTPUT:
                        OUTPUT.write(f"[ -f {SHELLUTIL['dst']} ] && . {SHELLUTIL['dst']}\n")

def shellutil_update(shellutil_id):

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM files WHERE id = ?', (shellutil_id,))
        row = cursor.fetchone()

        if row:
            column_names = [description[0] for description in cursor.description]

            SHELLUTIL = dict(zip(column_names, row))

            if SHELLUTIL['is_active']:

                if not os.path.exists(SHELLUTIL['dst']):
                    install_files([SHELLUTIL['name']])

                if SHELLUTIL['requires']:
                    requirements = SHELLUTIL['requires'].split(',')
                    requirements = [re.sub(r'\(.*?\)', '', item) for item in requirements]

                    # :/Required packages.
                    required_packages = [pkg.split('/')[1] for pkg in requirements if pkg.startswith('pkg')]
                    if required_packages:
                        install_packages(required_packages)

                    # :/Required files
                    required_files = [file.split('/')[1] for file in requirements if file.startswith('file')]
                    if required_files:
                        install_files(required_files)

            else:
                print(f"{SHELLUTIL['name']} is not active")

if __name__ == '__main__':
    shellutils_toggle('8')
