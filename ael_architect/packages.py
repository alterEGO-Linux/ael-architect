# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/packages.py]
# :author        : fantomH
# :created       : 2024-09-07 02:03:22 UTC
# :updated       : 2024-09-25 11:00:13 UTC
# :description   : Packages.

import os
import sqlite3
import subprocess
import tomllib

from config import AEL_DB

def packages_table():

    packages_file = '/usr/share/ael-config/packages.toml'

    with open(packages_file, mode='rb') as INPUT:
        data = tomllib.load(INPUT)

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                repo_archlinux TEXT NOT NULL,
                url TEXT,
                description TEXT,
                mode TEXT,
                requires TEXT,
                optional TEXT,
                notes TEXT
            )
        ''')

        for name, details in data.items():
            # :Check if the entry already exists.
            cursor.execute('SELECT id FROM packages WHERE name = ?', (name,))
            row = cursor.fetchone()

            if row:
                cursor.execute('''
                    UPDATE packages
                    SET repo_archlinux = ?, url = ?, description = ?, mode = ?, requires = ?, optional = ?, notes = ?
                    WHERE name = ?
                ''',
                (
                 details['repo_archilinux'],
                 details['url'],
                 details['description'],
                 ','.join(details['mode']) if details['mode'] else None,
                 ','.join(details['requires']) if details['requires'] else None,
                 ','.join(details['optional']) if details['optional'] else None,
                 ','.join(details['notes']) if details['notes'] else None,
                 name
                ))

            else:
                cursor.execute('''
                    INSERT INTO packages (name, repo_archlinux, url, description, mode, requires, optional, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (
                 name, 
                 details['repo_archlinux'],
                 details['url'],
                 details['description'],
                 ','.join(details['mode']) if details['mode'] else None,
                 ','.join(details['requires']) if details['requires'] else None,
                 ','.join(details['optional']) if details['optional'] else None,
                 ','.join(details['notes']) if details['notes'] else None,
                ))

        conn.commit()

def shell_utils_toggle(shell_util_id: str) -> None:

    table_shell_utils()
    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT is_active FROM scripts WHERE id = ?', (shell_util_id,))
        util = cursor.fetchone()

        if util:
            current_state = util[0]
            new_state = 0 if current_state == 1 else 1
            cursor.execute('''
                UPDATE scripts
                SET is_active = ?
                WHERE id = ?
            ''',
            (new_state, shell_util_id))

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
    packages_table()
