# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/aelinstall.py]
# :author        : fantomH
# :created       : 2024-10-14 12:41:19 UTC
# :updated       : 2024-10-14 12:41:24 UTC
# :description   : Archlinux basic installer.

"""
/ref/ https://github.com/archlinux/archinstall
"""

from pathlib import Path

from archinstall import Installer, profile
from archinstall import models
from archinstall.default_profiles.minimal import MinimalProfile
from archinstall.lib.disk.device_model import FilesystemType
from archinstall.lib.disk.encryption_menu import DiskEncryptionMenu
from archinstall.lib.disk.filesystem import FilesystemHandler
from archinstall.lib.interactions.disk_conf import select_disk_config

fs_type = FilesystemType('ext4')

# Select a device to use for the installation
disk_config = select_disk_config()

# Optional: ask for disk encryption configuration
data_store = {}
disk_encryption = DiskEncryptionMenu(disk_config.device_modifications, data_store).run()

# initiate file handler with the disk config and the optional disk encryption config
fs_handler = FilesystemHandler(disk_config, disk_encryption)

# perform all file operations
# WARNING: this will potentially format the filesystem and delete all data
fs_handler.perform_filesystem_operations()

mountpoint = Path('/tmp')

with Installer(
        mountpoint,
        disk_config,
        disk_encryption=disk_encryption,
        kernels=['linux']
) as installation:
    installation.mount_ordered_layout()
    installation.minimal_installation(hostname='minimal-arch')
    installation.add_additional_packages(['nano', 'wget', 'git'])

    # Optionally, install a profile of choice.
    # In this case, we install a minimal profile that is empty
    profile_config = profile.ProfileConfiguration(MinimalProfile())
    profile.profile_handler.install_profile_config(installation, profile_config)

    user = models.User('hacker1', 'password', True)
    installation.create_users(user)
