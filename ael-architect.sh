#!/usr/bin/env bash
# ------------------------------------------------------------------------ INFO
# [/ael-architect/ael-architect.sh]
# author        : Pascal Malouin @https://github.com/alterEGO-Linux
# created       : 2026-01-17 04:32:50 UTC
# updated       : 2026-01-23 04:58:31 UTC
# description   : Post Arch Linux install

set -euo pipefail

blue=$'\033[34m'
bold=$'\033[1m'
red=$'\033[31m'
reset=$'\033[0m'
yellow=$'\033[33m'

# -------------------- [ default configuration ]

AEL_USER="ghost"
AEL_USER_HOME="/home/${AEL_USER}"
AELFILES_GIT="https://github.com/alterEGO-Linux/ael-files.git"
AELFILES_DIRECTORY="${AEL_USER_HOME}/.local/share/ael-files"
AEL_DIRECTORY="${AEL_USER_HOME}/.ael"

# -------------------- [ rc files (/home) ]
AELFILES_RC_DIRECTORY="${AELFILES_DIRECTORY}/home"
AEL_RC_DIRECTORY="${AEL_USER_HOME}" 
AEL_RC_FILES=(
    .bashrc
    .profile
    .ael/.aelcore
    )
AEL_RC_SYMLINKED=true
AEL_RC_UPDATED_COPY=true

# -------------------- [ scripts (/bin) ]
AELFILES_BIN_DIRECTORY="${AELFILES_DIRECTORY}/bin"
AEL_BIN_DIRECTORY="${AEL_DIRECTORY}/bin"
AEL_BIN_APPS=(
    # --- ( busy.sh ) -> Look busy when the boss comes around.
    busy.sh

    # --- ( check-applications.sh ) -> Check applications' availability.
    check-applications.sh
    
    # --- ( convert-toml-json.py ) -> Convert TOML -> JSON
    convert-toml-json.py

    # --- ( convert-web-md.py ) -> Web to markdown converter.
    convert-web-md.py

    # --- ( dicom-tag.sh ) -> Search DICOM tags.
    dicom-tag.sh

    # --- ( docker-info.py ) -> Docker status helper.
    docker-info.py

    # --- ( extractor.sh ) -> Compressed files universal extractor.
    extractor.sh

    # --- ( menu-ael-files.sh ) -> Opens AEL files.
    menu-ael-files.sh

    # --- ( systeminfo.sh ) -> Gather system information.
    systeminfo.sh

    # --- ( tmuxplus.sh ) -> TMUX wrapper.
    tmuxplus.sh
    
    # --- ( translate.py) -> Translate using Google translate.
    translate.py

    # --- ( tunnel-info.py ) ->  Display Tunnels/VPN info.
    tunnel-info.py
    
    # --- ( virtual-boxes.sh ) -> Virtualbox VMs launcher.
    virtual-boxes.sh
    )
AEL_BIN_SYMLINKED=false
AEL_BIN_UPDATED_COPY=true

# -------------------- [ shellutils (/shellutils) ]

AELFILES_SHELLUTILS_DIRECTORY="${AELFILES_DIRECTORY}/shellutils"
AEL_SHELLUTILS_DIRECTORY="${AEL_DIRECTORY}/shellutils"
AEL_SHELLUTILS=(

    # --- ( ansi-colors ) -> ANSI colors helper.
    ansi-colors

    # --- ( deep-nmap ) -> Deep Nmap scan.
    deep-nmap

    # --- ( deep-scan ) -> Scans IP with rustscan and nmap.
    deep-scan

    # --- ( delete ) -> Delete directories.
    delete

    # --- (dircolors) -> Terminal colors.
    dircolors

    # --- ( directory-size ) -> Check size of biggest directories.
    directory-size

    # --- ( elevate ) -> Repeats last command with sudo, if forgotten.
    elevate

    # --- ( getmp3 ) -> Extracting audio (.mp3) from video.
    getmp3

    # --- ( goto ) -> Simple directory bookmarks system.
    goto

    # --- ( ispeed ) -> Internet connection speed meter.
    ispeed

    # --- ( pacman-reset ) -> Re-initialize pacman sync, mirrorlist and keyring.
    pacman-reset

    # --- ( ports ) -> Displays open ports.
    ports

    # --- ( processes ) -> Show processes.
    processes

    # --- ( ps-grep ) -> Show processes for a particular application.
    ps-grep

    # --- ( py-cleaner ) -> Clean python current directory.
    py-cleaner

    # --- ( py-server ) -> Create a Python HTTP server.
    py-server

    # --- ( reset-time ) -> Reset system time. Usefull when Windows boot screws time.
    reset-time

    # --- ( shell-info ) -> Show shell info.
    shell-info

    # --- ( show-utc ) -> Show UTC time.
    show-utc

    # --- ( snake-env ) -> Manage python -m venv.
    snake-env

    # --- ( termbin ) -> Netcat-based command-line pastebin.
    termbin

    # --- ( whoisweb ) -> Query WHOIS web if <whois> port 43 is blocked on your network.
    whoisweb

    # --- ( utils/ael-fzf ) -> FZF wrapper.
    # ... Utility wrapper around FZF, commenting out might keep other shellutils
    # ... from working properly.
    utils/ael-fzf

    # --- ( utils/argument-parser ) -> Argument parser utility.
    # ... Commenting out might keep other shellutils from working properly.
    utils/argument-parser

    # --- ( utils/check-applications ) -> A more verbose command -v.
    utils/check-applications
                  )
AEL_SHELLUTILS_SYMLINKED=true
AEL_SHELLUTILS_UPDATED_COPY=true

# -------------------- [ /.build ]
# --- Directory to build tools.
BUILD_DIRECTORY="${AEL_DIRECTORY}/.build"

# -------------------- [ AUR package manager ]
AUR_PKG_MANAGER_URL="https://aur.archlinux.org/paru.git"
AUR_PKG_MANAGER="paru"

# -------------------- [ end of configuration ]

# -------------------- [ utilities ]
copy_files() {

    local -n config="${1}"
    local -n files_list="${config[files]}"
    local src
    local dst
    local file

    for file in "${files_list[@]}"; do

        src="${config[src_directory]}/${file}"
        dst="${config[dst_directory]}/${file}"

        [ -e "${src}" ] || continue

        # --- symlink
        if [ "${config[symlinked]}" == true  ]; then
            # --- verify if symlink.
            if [ -L "${dst}" ]; then
                # --- verify if dst points somewhere else, fix it.
                if [ "$(readlink -f -- "${dst}")" != "${src}" ]; then
                    ln -sfn "${src}" "${dst}"
                fi
            else
                # --- remove regular file if exist and create symlink.
                [ -e "${dst}" ] && rm -rf -- "${dst}"
                ln -s "${src}" "${dst}"
            fi
        else
            # --- remove symlink if exist.
            [ -L "${dst}" ] && rm -f -- "${dst}"

            if [ -f "${dst}" ]; then
                # --- keep copy updated?
                if [ "${config[updated_copy]}" == true ]; then
                    if [ "$(readlink -f -- "${dst}")" != "$(readlink -f -- "${src}")" ]; then
                        # --- copy only if content differs.
                        if ! cmp -s "${src}" "${dst}"; then
                            cp -f "${src}" "${dst}"
                        fi
                    fi
                fi
            else
                # --- make a copy.
                cp "${src}" "${dst}"
            fi
        fi

    done
}

require_user() {
    local allowed_user="${1:?missing allowed user}"
    local action="${2:?missing action description}"
    local current_user

    current_user="$(id -un)"

    case "${allowed_user}" in
        root)
            if [[ $EUID -ne 0 ]]; then
                printf "%s\n" "${red}[!]${reset} ${action} can only be run by root."
                exit 1
            fi
            ;;
        "$AEL_USER")
            if [[ "${current_user}" != "${AEL_USER}" ]]; then
                printf "%s\n" "${red}[!]${reset} ${action} can only be run by ${AEL_USER}."
                exit 1
            fi
            ;;
        *)
            printf "%s\n" "${red}[!]${reset} Invalid allowed user: ${allowed_user}."
            exit 1
            ;;
    esac
}

fix_ownership() {
    # --- fixes ownership recursively to the ael user.
    # ... ex: fix_ownership ghost ~/.local/share/ael-files

    local user="${1:?missing user}"
    local path="${2:-.}"
    local group

    group="$(id -gn "$user")"

    find "$path" \
      \( ! -user "$user" -o ! -group "$group" \) \
      -exec chown "$user:$group" {} +
}

__extract_vars_from_cmd() {
    # Extract variable names used in a command string ($VAR and ${VAR})
    local cmd="$1"

    # 1) ${VAR} patterns
    # 2) $VAR patterns (skip $1, $?, $$, $@, etc. by only allowing [A-Za-z_])
    printf '%s\n' "$cmd" |
        grep -oE '\$\{[A-Za-z_][A-Za-z0-9_]*\}|\$[A-Za-z_][A-Za-z0-9_]*' |
        sed -E 's/^\$\{?//; s/\}?$//; s/^\$//' |
        sort -u
}

run_as_ael_user() {
    local user="${AEL_USER:?AEL_USER not set}"
    local cmd="${1:?missing command}"

    # Already running as the target user → run directly
    if [[ "$(id -un)" == "$user" ]]; then
        bash -lc "$cmd"
        return
    fi

    # Need privilege to switch users
    [[ $EUID -ne 0 ]] && { echo "Need root to run as $user"; return 1; }

    # Build env args only for vars referenced in cmd and defined in this shell
    local -a env_args=(env)
    local var
    while IFS= read -r var; do
        # Only pass through vars that are set in the current shell
        # (so we don't trigger nounset issues when composing env)
        if [[ -v $var ]]; then
            env_args+=("$var=${!var}")
        fi
    done < <(__extract_vars_from_cmd "$cmd")

    sudo -u "$user" "${env_args[@]}" bash -lc "$cmd"
}

# -------------------- [ ael configuration ]

pull_aelfiles() {

    require_user $AEL_USER "Getting AEL files"

    mkdir -p ${AEL_USER_HOME}/.local/share

    if [[ ! -d ${AELFILES_DIRECTORY}/.git ]]; then
        git clone ${AELFILES_GIT} ${AELFILES_DIRECTORY}
    else
        cd "$AELFILES_DIRECTORY"
        git pull
    fi

}

install_aur_pkg_manager() {

    require_user "${AEL_USER}" "AUR package manager installation"

    if ! command -v ${AUR_PKG_MANAGER} >/dev/null 2>&1; then
        mkdir -p $BUILD_DIRECTORY
        cd $BUILD_DIRECTORY
        git clone $AUR_PKG_MANAGER_URL $AUR_PKG_MANAGER
        cd $AUR_PKG_MANAGER
        makepkg -si --noconfirm
    fi
}

set_rc(){

    require_user $AEL_USER "Setting up home"

    local rc directory

    local -A cfg=(
        [src_directory]="${AELFILES_RC_DIRECTORY}"
        [dst_directory]="${AEL_RC_DIRECTORY}"
        [symlinked]="${AEL_RC_SYMLINKED}"
        [updated_copy]="${AEL_RC_UPDATED_COPY}"
        )

    local -a files_rc=("${AEL_RC_FILES[@]}")
    cfg[files]=files_rc

    # --- make sure to backup non AEL bashrc and profile.
    for rc in "$AEL_USER_HOME/.bashrc" "$AEL_USER_HOME/.profile"; do
        [[ -f "$rc" ]] || continue

        if ! grep -q "alterEGO-Linux" "$rc"; then
            mv "$rc" "$rc.aelbkp"
        fi
    done

    # --- create necessary subdirectories.
    for directory in .ael; do
        mkdir -p "${AEL_RC_DIRECTORY}/$directory"
    done

    copy_files cfg
}

set_bin() {

    require_user $AEL_USER "Setting up bin"

    local file

    local -A cfg=(
        [src_directory]="${AELFILES_BIN_DIRECTORY}"
        [dst_directory]="${AEL_BIN_DIRECTORY}"
        [symlinked]="${AEL_BIN_SYMLINKED}"
        [updated_copy]="${AEL_BIN_UPDATED_COPY}"
        )

    local -a files_bin=("${AEL_BIN_APPS[@]}")
    cfg[files]=files_bin

    mkdir -p "${AEL_BIN_DIRECTORY}"

    copy_files cfg

    # --- make applications executable.
    for file in "${AEL_BIN_APPS[@]}"; do
        [[ -L "${AEL_BIN_DIRECTORY}/${file}" ]] || chmod +x "${AEL_BIN_DIRECTORY}/${file}"
    done

}

set_shellutils() {

    require_user $AEL_USER "Setting up Shellutils"

    local directory utils

    local -A cfg=(
        [src_directory]="${AELFILES_SHELLUTILS_DIRECTORY}"
        [dst_directory]="${AEL_SHELLUTILS_DIRECTORY}"
        [symlinked]="${AEL_SHELLUTILS_SYMLINKED}"
        [updated_copy]="${AEL_SHELLUTILS_UPDATED_COPY}"
        )

    local -a files_shellutils=("${AEL_SHELLUTILS[@]}")
    cfg[files]=files_shellutils

    # --- create necessary subdirectories.
    for directory in utils; do
        mkdir -p "${AEL_SHELLUTILS_DIRECTORY}/$directory"
    done

    copy_files cfg
}

# -------------------- [ installer ]

create_user() {

    require_user root "Creating new user"

    pull_aelfiles
    
    local user="${AEL_USER:-ael}"
    local sudoers_file="/etc/sudoers.d/${AEL_USER}"

    # --- create user if missing.
    if ! id "${AEL_USER}" &>/dev/null; then
        useradd \
            --create-home \
            --shell /bin/bash \
            --groups wheel \
            "${AEL_USER}"
    else
        # --- Ensure wheel group membership
        usermod -aG wheel "${AEL_USER}"
    fi

    # --- configure passwordless sudo.
    if [[ ! -f "${sudoers_file}" ]]; then
        echo "${AEL_USER} ALL=(ALL) NOPASSWD: ALL" > "${sudoers_file}"
        chmod 0440 "${sudoers_file}"
    fi
}

# -------------------- [ options ]

create_config_file() {
    local src_config="$(realpath "$0")"
    local config_file="ael.conf"

    awk '
      /\[ default configuration \]/ {flag=1; next}
      /\[ end of configuration \]/ {flag=0}
      flag
    ' "$src_config" > "$config_file"

    printf "%s\n" "${blue}[*]${reset} ${config_file} created."
    
}

configure_ael() {

    require_user ${AEL_USER} "AEL Post-installation"

    pull_aelfiles    
    install_aur_pkg_manager
    set_rc
    set_bin
    set_shellutils

}

option_parser() {

    if [[ "${CREATE_CONFIG_FILE}" == true ]]; then
        create_config_file
        exit 0
    fi

    if [[ "${AEL_CONFIGURATION}" == true ]]; then
        configure_ael
        exit 0
    fi

    if [[ "${UPDATE}" == true ]]; then
        set_shellutils
        set_bin
        exit 0
    fi

    if [[ "${CREATE_USER}" == true ]]; then
        create_user
    fi

    if [[ "${PULL_AELFILES}" == true ]]; then
        pull_aelfiles
    fi

    if [[ "${INSTALL_AUR_PKG_MANAGER}" == true ]]; then
        install_aur_pkg_manager
    fi

}

CREATE_CONFIG_FILE=false
CREATE_USER=false
AEL_CONFIGURATION=false
INSTALL_AUR_PKG_MANAGER=false
PULL_AELFILES=false
UPDATE=false
for arg in "${@}"; do
    case "${arg}" in
        --create-config-file)
            CREATE_CONFIG_FILE=true
            option_parser
            ;;
        --create-user)
            CREATE_USER=true
            option_parser
            ;;
        --install-aur-pkg-manager)
            INSTALL_AUR_PKG_MANAGER=true
            option_parser
            ;;
        --ael-configuration)
            AEL_CONFIGURATION=true
            option_parser
            ;;
        --pull-aelfiles)
            PULL_AELFILES=true
            option_parser
            ;;
        --update)
            UPDATE=true
            option_parser
            ;;
        *)
            echo wrong
            ;;
    esac
done
