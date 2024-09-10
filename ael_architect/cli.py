# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/cli.py]
# :author        : fantomH
# :created       : 2024-09-06 15:27:10 UTC
# :updated       : 2024-09-06 15:27:17 UTC
# :description   : cli.

import curses
import subprocess

from database import dict_shell_utils
from database import toggle_shell_util
from database import shell_utils_requirements
from shell_utils import install_shell_util

def draw_menu(stdscr):
    # Clear the screen
    stdscr.clear()

    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    # Get screen height and width
    height, width = stdscr.getmaxyx()

    # Calculate window dimensions
    mid_x = width // 4
    padding = 2

    # Create left and right windows
    left_win = stdscr.subwin(height, mid_x, 0, 0)
    right_win = stdscr.subwin(height, width - mid_x, 0, mid_x)

    menu_win = left_win.subwin(height - 2 * padding, mid_x - 2 * padding, padding, padding)
    menu_win.box()

    menu_options = ['Shell Utils', 'Option 2', 'Option 3', 'Option 4']
    menu_selection = 0

    shell_utils_items = dict_shell_utils()
    shell_utils_selection = 0
    scroll_position = 0

    WINDOW_FOCUS = 'menu'

    def update_menu_win():
        menu_win.clear()
        menu_win.box()

        for idx, option in enumerate(menu_options):
            if idx == menu_selection:
                menu_win.addstr(idx + 2, 2, option, curses.A_REVERSE)
            else:
                menu_win.addstr(idx + 2, 2, option)

    def update_right_win():
        right_win.clear()
        if menu_selection == 0:
            visible_items = shell_utils_items[scroll_position:scroll_position + (height // 3) - 1]
            for idx, item in enumerate(visible_items):
                button_state = 'On' if item['is_active'] else 'Off'
                actual_index = scroll_position + idx
                if actual_index == shell_utils_selection:
                    right_win.addstr(idx * 3 + 2, 2, f"{item['name']}", curses.A_BOLD)
                    right_win.addstr(idx * 3 + 2, 50, f"{button_state}", curses.A_REVERSE)
                    right_win.addstr(idx * 3 + 3, 2, f"{item['description']}")
                else:
                    right_win.addstr(idx * 3 + 2, 2, f"{item['name']}", curses.A_BOLD)
                    right_win.addstr(idx * 3 + 2, 50, f"{button_state}")
                    right_win.addstr(idx * 3 + 3, 2, f"{item['description']}")
        else:
            right_win.addstr(2, 0, f"Details for {menu_selection}")
        right_win.refresh()

    def run_paru_overlay(shell_util_id):
        overlay_height = height // 2
        overlay_width = width // 2
        overlay_win = stdscr.subwin(overlay_height, overlay_width, height // 4, width // 4)
        overlay_win.box()
        overlay_win.refresh()

        requirements = shell_utils_requirements(shell_utils_items[shell_utils_selection]['id'])

        if requirements:
            command = ['paru', '-S', '--noconfirm', '--needed'] + requirements
        else:
            command = ['echo']

        paru_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = []

        while True:
            stdscr.refresh()
            left_win.refresh()
            right_win.refresh()
            overlay_win.refresh()

            line = paru_process.stdout.readline()
            if not line and paru_process.poll() is not None:
                break

            output.append(line.strip())
            if len(output) > overlay_height - 2:
                output.pop(0)

            overlay_win.clear()
            overlay_win.box()

            for idx, line in enumerate(output):
                overlay_win.addstr(idx + 1, 1, line)

            overlay_win.refresh()

        paru_process.stdout.close()
        paru_process.stderr.close()
        overlay_win.clear()
        stdscr.clear()
        update_menu_win()
        update_right_win()

    while True:
        update_menu_win()
        menu_win.refresh()
        left_win.refresh()
        stdscr.refresh()

        if WINDOW_FOCUS == 'shell_utils':
            key = stdscr.getch()

            if key == curses.KEY_UP:
                if shell_utils_selection > 0:
                    shell_utils_selection -= 1
                    if shell_utils_selection < scroll_position:
                        scroll_position -= 1
                update_right_win()
            elif key == curses.KEY_DOWN:
                if shell_utils_selection < len(shell_utils_items) - 1:
                    shell_utils_selection += 1
                    if shell_utils_selection >= scroll_position + (height // 3) - 1:
                        scroll_position += 1
                update_right_win()
            elif key == ord('\n'):
                toggle_shell_util(shell_utils_items[shell_utils_selection]['id'])
                install_shell_util(shell_utils_items[shell_utils_selection]['id'])
                shell_utils_items = dict_shell_utils()
                update_right_win()
                run_paru_overlay(shell_utils_items[shell_utils_selection]['id'])
            elif key == ord('q'):
                break
            else:
                WINDOW_FOCUS = 'menu'
        else:
            key = stdscr.getch()

            if key == curses.KEY_UP:
                menu_selection = (menu_selection - 1) % len(menu_options)
            elif key == curses.KEY_DOWN:
                menu_selection = (menu_selection + 1) % len(menu_options)
            elif key == ord('q'):
                break
            elif key == ord('\n'):
                WINDOW_FOCUS = 'shell_utils'
                update_right_win()

    # if right_win_focus:
        # update_right_win()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
