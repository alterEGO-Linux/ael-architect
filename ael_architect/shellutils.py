# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/shellutils.py]
# :author        : fantomH
# :created       : 2024-09-07 02:03:22 UTC
# :updated       : 2024-09-08 14:16:01 UTC
# :description   : database.

import os
import sqlite3
import subprocess
import tomllib

from config import AEL_DB

def shellutils_table():

    shellutils_file = '/usr/share/ael/shellutils.toml'

    with open(shellutils_file, mode='rb') as INPUT:
        data = tomllib.load(INPUT)

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shellutils (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                filename TEXT NOT NULL,
                url TEXT,
                description TEXT,
                mode TEXT,
                requires TEXT,
                optional TEXT,
                is_active BOOLEAN NOT NULL DEFAULT False
            )
        ''')

        for name, details in data.items():
            # :/Check if the entry already exists.
            cursor.execute('SELECT id FROM shellutils WHERE name = ?', (name,))
            row = cursor.fetchone()

            if row:
                cursor.execute('''
                    UPDATE shellutils
                    SET filename = ?, url = ?, description = ?, mode = ?, requires = ?, optional = ?
                    WHERE name = ?
                ''',
                (details['filename'],
                details['url'],
                details['description'],
                ','.join(details['mode']) if details['mode'] else None,
                ','.join(details['requires']) if details['requires'] else None,
                ','.join(details['optional']) if details['optional'] else None,
                name))

            else:
                cursor.execute('''
                    INSERT INTO shellutils (name, filename, url, description, mode, requires, optional, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (name, 
                details['filename'], 
                details['url'], 
                details['description'], 
                ','.join(details['mode']) if details['mode'] else None,
                ','.join(details['requires']) if details['requires'] else None,
                ','.join(details['optional']) if details['optional'] else None,
                False))

        conn.commit()

def shellutils_to_listdicts():

    shellutils_table()
    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM shellutils')
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        _shellutils = [dict(zip(column_names, row)) for row in rows]

        _shellutils.sort(key=lambda x: x['name'])

        return _shellutils

def shellutils_toggle(shellutil_id: str) -> None:

    """
    Used by sysconfig.py to activate/deactivate a Shell Util.
    """

    shellutils_table()
    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT is_active FROM shellutils WHERE id = ?', (shellutil_id,))
        util = cursor.fetchone()

        if util:
            current_state = util[0]
            new_state = 0 if current_state == 1 else 1
            cursor.execute('''
                UPDATE shellutils
                SET is_active = ?
                WHERE id = ?
            ''',
            (new_state, shellutil_id))

        conn.commit()

def shell_utils_requirements(shell_util_id):

    table_shell_utils()
    table_packages()

    requirements = []

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT name FROM scripts WHERE id = ?', (shell_util_id,))
        util = cursor.fetchone()[0]

        # :---/ requirements /---:

        query = """
            SELECT *
            FROM packages
            WHERE ',' || ael_scripts || ',' LIKE ?
            """

        cursor.execute(query, (f'%,{util},%',))

        results = cursor.fetchall()

        if results:
            column_names = [description[0] for description in cursor.description]
            results = [dict(zip(column_names, row)) for row in results]

            for x in results:
                requirements.append(x['name'])

            # return requirements

            command = ['paru', '-S', '--noconfirm', '--needed'] + requirements

            try:
                result = subprocess.run(
                            command,
                            check=True,
                            text=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            )
                print("Packages installed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while installing packages: {e}")

if __name__ == '__main__':
    print(shellutils_to_listdicts())
