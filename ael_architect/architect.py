# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/architect.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2024-12-11 11:28:21 UTC
# :description   : Main.

import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser(description="AEL Architect.")

    parser.add_argument('--config', help="Path to custom ael.toml configuration file.")

    args = parser.parse_args()

if __name__ == "__main__":
    main()
