# :----------------------------------------------------------------------- INFO
# :[ael_architect/control_panel.py]
# :author        : AlterEgo Linux
# :created       : 2025-03-13 09:12:19 UTC
# :updated       : 2025-03-15 15:17:14 UTC
# :description   : Control Panel

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, ContentSwitcher, DataTable, Markdown, Footer, Header, Static

MARKDOWN_EXAMPLE = """# Three Flavours Cornetto

The Three Flavours Cornetto trilogy is an anthology series of British
comedic genre films directed by Edgar Wright.

## Shaun of the Dead

| Flavour | UK Release Date | Director |
| -- | -- | -- |
| Strawberry | 2004-04-09 | Edgar Wright |

## Hot Fuzz

| Flavour | UK Release Date | Director |
| -- | -- | -- |
| Classico | 2007-02-17 | Edgar Wright |

## The World's End

| Flavour | UK Release Date | Director |
| -- | -- | -- |
| Mint | 2013-07-19 | Edgar Wright |
"""

class Menu(Vertical):
    def compose(self) -> ComposeResult:
        yield Button("Info", id="info")
        yield Button("DataTable", id="data-table")
        yield Button("Markdown", id="markdown")

class SystemInfo(Vertical):
    def get_distro_name(self):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME"):
                    return line.strip().split("=")[1].strip('"')

    kernel_version = f"1.0"

    def compose(self) -> ComposeResult:
        yield Static(f"OS: {self.get_distro_name()}")
        yield Static(f"Kernel Version: {SystemInfo.kernel_version}")

class ControlPanelApp(App[None]):
    CSS = """
Screen {
    padding: 1;
}

Menu Button {
    width: 1fr;
}

ContentSwitcher {
    width: 3fr;
    border: round $primary;
    height: 1fr;
    padding-left: 4;
}

MarkdownH2 {
    background: $panel;
    color: yellow;
    border: none;
    padding: 0 1;
}

"""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            # Left pane for buttons
            yield Menu(id="buttons")
            # Right pane for content
            with ContentSwitcher(initial="info", id="content-switcher"):
                yield SystemInfo(id="info")
                yield DataTable(id="data-table")
                with VerticalScroll(id="markdown"):
                    yield Markdown(MARKDOWN_EXAMPLE)
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id  

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Book", "Year")
        table.add_rows(
            [
                (title.ljust(35), year)
                for title, year in (
                    ("Dune", 1965),
                    ("Dune Messiah", 1969),
                    ("Children of Dune", 1976),
                    ("God Emperor of Dune", 1981),
                    ("Heretics of Dune", 1984),
                    ("Chapterhouse: Dune", 1985),
                )
            ]
        )

if __name__ == "__main__":
    app = ControlPanelApp()
    app.run()


# from textual.app import App, ComposeResult
# from textual.containers import Container, Horizontal, Vertical, VerticalScroll
# from textual.widgets import Header, Footer, Button, Static
# import platform
# import socket

# class SideMenu(Container):

    # def compose(self) -> ComposeResult:
        # yield Button("Info", id="info")
        # yield Button("General", id="general")
        # yield Button("Shellutils", id="shellutils")
        # yield Button("Applications", id="applications")

# class ContentArea(Static):

    # def update_content(self, content: Static) -> None:
        # self.remove_children()
        # self.mount(content)

# def get_system_info() -> VerticalScroll:
    # os_info = platform.system() + " " + platform.release()
    # kernel_version = platform.version()
    # try:
        # ip_address = socket.gethostbyname(socket.gethostname())
    # except socket.gaierror:
        # ip_address = "Unavailable"

    # container = VerticalScroll(
        # Static(f"OS: {os_info}"),
        # Static(f"Kernel Version: {kernel_version}"),
        # Static(f"IP Address: {ip_address}")
    # )
    # return container

# class ControlPanelApp(App):
    # CSS = """
    # SideMenu {
        # dock: left;
        # width: 30;
        # height: 100%;
        # background: #2e2e2e;
        # color: white;
    # }

    # SideMenu.-hidden {
        # display: none;
    # }
    # SideMenu Button {
        # width: 100%;
        # padding: 1;
        # background: transparent;
        # color: white;
        # border: none;
    # }

    # SideMenu Button:hover {
        # background: #3e3e3e;
    # }

    # SideMenu Button:focus {
        # background: $boost;
    # }

    # ContentArea {
        # padding: 1;
    # }
    # """

    # BINDINGS = [("ctrl+s", "toggle_menu")]

    # def compose(self) -> ComposeResult:
        # yield Header()
        # self.side_menu = SideMenu()
        # yield self.side_menu
        # self.content_area = ContentArea()
        # yield self.content_area
        # yield Footer()

    # def on_button_pressed(self, event: Button.Pressed) -> None:
        # button_id = event.button.id
        # if button_id:
            # Remove '-focus' class from all buttons first
            # for button in self.side_menu.query(Button):
                # button.remove_class("focus")
            # Add '-active' class to the clicked button
            # event.button.add_class("focus")
            # Update the content area
            # if button_id == "info":
                # self.content_area.update_content(get_system_info())
            # else:
                # self.content_area.update_content(Static(f"Selected: {button_id.capitalize()}"))

    # def action_toggle_menu(self) -> None:
        # self.query_one(SideMenu).toggle_class("-hidden")

