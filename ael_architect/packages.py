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
from utils import get_linux_id

def packages_table():

    packages_file = '/usr/share/ael/packages.toml'

    with open(packages_file, mode='rb') as INPUT:
        data = tomllib.load(INPUT)

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                archlinux TEXT NOT NULL,
                url TEXT,
                description TEXT,
                modes TEXT,
                requires TEXT,
                optional TEXT,
                is_installed BOOLEAN NOT NULL DEFAULT False,
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
                    SET archlinux = ?,
                        url = ?,
                        description = ?,
                        modes = ?,
                        requires = ?,
                        optional = ?,
                        notes = ?
                    WHERE name = ?
                ''',
                (
                 details['archlinux'],
                 details['url'],
                 details['description'],
                 ','.join(details['modes']) if details['modes'] else None,
                 ','.join(details['requires']) if details['requires'] else None,
                 ','.join(details['optional']) if details['optional'] else None,
                 ','.join(details['notes']) if details['notes'] else None,
                 name
                ))

            else:
                cursor.execute('''
                    INSERT INTO packages (name, 
                                          archlinux, 
                                          url, 
                                          description,
                                          modes,
                                          requires,
                                          optional,
                                          notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (
                 name, 
                 details['archlinux'],
                 details['url'],
                 details['description'],
                 ','.join(details['modes']) if details['modes'] else None,
                 ','.join(details['requires']) if details['requires'] else None,
                 ','.join(details['optional']) if details['optional'] else None,
                 ','.join(details['notes']) if details['notes'] else None,
                ))

        conn.commit()

    packages_installed()

def packages_to_listdicts():

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM packages")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        PACKAGES = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            PACKAGES.append(row_dict)

        PACKAGES.sort(key=lambda x: x['name'])

        return PACKAGES

def packages_installed():

    linux_id = get_linux_id()

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM packages")
        rows = cursor.fetchall()

        column_names = [description[0] for description in cursor.description]

        for row in rows:
            PACKAGE = dict(zip(column_names, row))

            if linux_id in ['arch', 'ael', 'manjaro']:
                PKG = PACKAGE['archlinux'].split('/')[1].replace('base(', '').replace('base-devel(', '').replace(')', '')
                result = subprocess.run(['pacman', '-Qq', PKG], capture_output=True, text=True)

                if result.stdout.strip():
                    PACKAGE['is_installed'] = True
                else:
                    PACKAGE['is_installed'] = False

            cursor.execute('''
                UPDATE packages
                SET is_installed = ?
                WHERE name = ?
            ''',
            (
                PACKAGE['is_installed'],
                PACKAGE['name']
            ))

if __name__ == '__main__':
    packages_installed()
