# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/aelinstall.py]
# :author        : fantomH
# :created       : 2024-10-14 12:41:19 UTC
# :updated       : 2024-10-14 12:41:24 UTC
# :description   : Archlinux basic installer.

import archinstall

def ask_user():
    # Ask the user for installation details interactively
    print("Arch Linux Installation")

    # List available disks and prompt user for disk selection
    available_disks = archinstall.list_disks()
    if not available_disks:
        raise SystemExit("No disks found! Exiting...")

    print("\nAvailable Disks:")
    for index, disk in enumerate(available_disks):
        print(f"{index + 1}: {disk}")

    disk_choice = int(input("Select disk number (e.g., 1): ")) - 1
    selected_disk = available_disks[disk_choice]

    # Ask for language and timezone
    language = input("Enter language (e.g., en_US): ") or "en_US"
    timezone = input("Enter timezone (e.g., Europe/Paris): ") or "UTC"

    # Prompt for root password
    root_password = input("Enter root password: ")

    # Prompt for hostname
    hostname = input("Enter hostname for the system: ") or "archlinux"

    # Prompt for a user to create
    username = input("Enter username to create (optional): ")

    # Prompt for additional packages
    additional_packages = input("Enter additional packages to install (comma separated, e.g., vim,git): ").split(',')

    return {
        "disk": selected_disk,
        "language": language,
        "timezone": timezone,
        "root_password": root_password,
        "hostname": hostname,
        "username": username,
        "additional_packages": additional_packages
    }


def install_arch(settings):
    # Start installation with the provided settings
    with archinstall.Installer(settings['disk'], boot_mode=archinstall.GPT) as installation:
        installation.set_locale(settings['language'])
        installation.set_hostname(settings['hostname'])
        installation.set_timezone(settings['timezone'])

        # Set root password
        installation.set_root_password(settings['root_password'])

        # Partition the disk (using autopartition)
        archinstall.storage.autopartition(settings['disk'], wipe=True)

        # Install base system
        installation.install_profile('minimal')
        
        # Add additional packages if any
        if settings['additional_packages']:
            installation.add_additional_packages(settings['additional_packages'])

        # Set up user account if provided
        if settings['username']:
            user_password = input(f"Enter password for {settings['username']}: ")
            installation.add_user(settings['username'], user_password)

        # Finalize installation
        if installation.has_minimal_install():
            print("Arch Linux has been installed successfully.")
            installation.configure_bootloader()
        else:
            raise SystemExit("Installation failed!")


if __name__ == "__main__":
    # Get user settings
    user_settings = ask_user()
    # Start the installation process
    install_arch(user_settings)
