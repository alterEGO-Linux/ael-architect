# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/cli.py]
# :author        : fantomH
# :created       : 2024-09-06 15:27:10 UTC
# :updated       : 2024-09-06 15:27:17 UTC
# :description   : cli.

import curses

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

    menu_options = ['Option 1', 'Option 2', 'Option 3', 'Option 4']
    menu_selection = 0

    shell_utils_items = [
                         {'name': 'shell-info', 'button': False, 'description': 'description 1'},
                         {'name': 'systeminfo', 'button': False, 'description': 'description 2'}
                        ]
    shell_utils_selection = 0

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
            for idx, item in enumerate(shell_utils_items):
                button_state = 'On' if item['button'] else 'Off'
                if idx == shell_utils_selection:
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

    while True:
        update_menu_win()
        menu_win.refresh()
        left_win.refresh()
        stdscr.refresh()

        if WINDOW_FOCUS == 'shell_utils':
            key = stdscr.getch()

            if key == curses.KEY_UP:
                shell_utils_selection = (shell_utils_selection - 1) % len(shell_utils_items)
                update_right_win()
            elif key == curses.KEY_DOWN:
                shell_utils_selection = (shell_utils_selection + 1) % len(shell_utils_items)
                update_right_win()
            elif key == ord('\n'):
                shell_utils_items[shell_utils_selection]['button'] = not shell_utils_items[shell_utils_selection]['button']
                update_menu_win()
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
