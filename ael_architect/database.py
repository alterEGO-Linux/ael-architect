# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/database.py]
# :author        : fantomH
# :created       : 2024-09-07 02:03:22 UTC
# :updated       : 2024-09-07 02:03:26 UTC
# :description   : database.

import os
import sqlite3
import tomllib

from config import AEL_DB

def update_shell_utils():

    with open('/home/ghost/main/ael-architect/data/scripts.toml', mode='rb') as INPUT:
        data = tomllib.load(INPUT)

        print(data)

    conn = sqlite3.connect(AEL_DB)
    cursor = conn.cursor()

    # Create a table for the scripts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            filename TEXT NOT NULL,
            url TEXT,
            description TEXT,
            mode TEXT
        )
    ''')

    # Insert data from TOML into SQLite
    for name, details in data.items():
        cursor.execute('''
            INSERT INTO scripts (name, filename, url, description, mode)
            VALUES (?, ?, ?, ?, ?)
        ''', 
        (name, 
        details['filename'], 
        details['url'], 
        details['description'], 
        ','.join(details['mode']) if details['mode'] else None))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_shell_utils()

