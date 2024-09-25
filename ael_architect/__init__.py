# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/__init__.py]
# :author        : fantomH
# :created       : 2024-09-06 15:17:01 UTC
# :updated       : 2024-09-25 12:09:40 UTC
# :description   : Main.

import argparse
from sysconfig import run_sysconfig

def start_gui_app():
    print("Starting GUI app...")

def main():
    parser = argparse.ArgumentParser(description="AEL Architect.")
    
    parser.add_argument('--gui', action='store_true', help="Start the GUI app instead of the CLI app.")
    
    args = parser.parse_args()
    
    if args.gui:
        start_gui_app()
    else:
        run_sysconfig()

if __name__ == "__main__":
    main()
