# :----------------------------------------------------------------------- INFO
# :[Snake-Vault/snake_vault/installer.py]
# :author        : fantomH
# :created       : 2024-04-10 11:56:42 UTC
# :updated       : 2024-04-10 11:56:42 UTC
# :description   : alterEGO linux installer.

import argparse
import importlib.util
import json

from command import execute

def load_config(config_path):

    spec = importlib.util.spec_from_file_location("config", config_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module

class Installer:

    def __init__(self, config):

        self.config = config

    def get_disk(self):
        cmd = f"lsblk --output TRAN,NAME,PATH,ID-LINK,SIZE,STATE,PARTTYPENAME,UUID,PTTYPE,FSTYPE,TYPE,MOUNTPOINTS --json --tree"
        json_string = execute(cmd, text=True).stdout
        data = json.loads(json_string)

        return data
    
def main():
    parser = argparse.ArgumentParser(description="Installer")
    parser.add_argument("-c", "--config", help="Path to custom config file.")
    args = parser.parse_args()

    # :Load the configuration file
    if args.config:
        config_path = args.config
    else:
        config_path = "config.py"  # Default config file path
    config = load_config(config_path)

    installer = Installer(config)

    print(installer.get_disk())
    # print([x for x in config])

    # Access the user_name list from the loaded configuration file
    # TIMEZONE = config.TIMEZONE

    # Do whatever you need with the user_names
    # print(type(TIMEZONE))

if __name__ == "__main__":
    main()

# :------------------------------------------------------------- FIN ¯\_(ツ)_/¯
