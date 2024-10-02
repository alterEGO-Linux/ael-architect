# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/files.py]
# :author        : fantomH
# :created       : 2024-09-29 13:12:46 UTC
# :updated       : 2024-09-29 13:12:51 UTC
# :description   : Files.

# import os
import sqlite3
# import subprocess
import tomllib

from config import AEL_DB

def files_table():

    SRC = '/usr/share/ael/files.toml'

    with open(SRC, mode='rb') as INPUT:
        data = tomllib.load(INPUT)

    with sqlite3.connect(AEL_DB) as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT,
                src TEXT,
                dst TEXT,
                description TEXT,
                modes TEXT,
                is_symlink BOOLEAN NOT NULL DEFAULT False,
                create_bkp BOOLEAN NOT NULL DEFAULT False,
                notes TEXT
            )
        ''')

        for name, details in data.items():
            # :Check if the entry already exists.
            cursor.execute('SELECT id FROM files WHERE name = ?', (name,))
            row = cursor.fetchone()

            if row:
                cursor.execute('''
                    UPDATE files
                    SET url = ?, src = ?, dst = ?, description = ?, modes = ?, is_symlink = ?, create_bkp = ?, notes = ?
                    WHERE name = ?
                ''',
                (
                 details['url'],
                 details['src'],
                 details['dst'],
                 details['description'],
                 ','.join(details['modes']) if details['modes'] else None,
                 details['is_symlink'],
                 details['create_bkp'],
                 ','.join(details['notes']) if details['notes'] else None,
                 name
                ))

            else:
                cursor.execute('''
                    INSERT INTO files (name, url, src, dst, description, modes, is_symlink, create_bkp, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (
                 name, 
                 details['url'],
                 details['src'],
                 details['dst'],
                 details['description'],
                 ','.join(details['modes']) if details['modes'] else None,
                 details['is_symlink'],
                 details['create_bkp'],
                 ','.join(details['notes']) if details['notes'] else None,
                ))

        conn.commit()

if __name__ == '__main__':
    files_table()
