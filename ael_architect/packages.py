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

if __name__ == '__main__':
    packages_table()
