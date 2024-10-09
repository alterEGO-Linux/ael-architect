# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/sysconfig.py]
# :author        : fantomH
# :created       : 2024-09-06 15:27:10 UTC
# :updated       : 2024-09-10 11:54:26 UTC
# :description   : cli.

import asyncio

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.containers import Vertical
from textual.widgets import Footer
from textual.widgets import Label
from textual.widgets import Markdown
from textual.widgets import ProgressBar
from textual.widgets import TabbedContent
from textual.widgets import TabPane
from textual.widgets import Static
from textual.widgets import Switch

from files import files_table
from packages import packages_table
from packages import packages_to_listdicts
from shellutils import shellutils_to_listdicts
from shellutils import shellutils_toggle

files_table()
packages_table()

SHELLUTILS = shellutils_to_listdicts()
PACKAGES = packages_to_listdicts()

JESSICA = """
# Lady Jessica

Bene Gesserit and concubine of Leto, and mother of Paul and Alia.
"""

PAUL = """
# Paul Atreides

Son of Leto and Jessica.
"""


class TabbedApp(App):
    """An example of tabbed content."""

    BINDINGS = [
        ("s", "show_tab('shell-utils')", "SHELL-UTIL"),
        ("j", "show_tab('jessica')", "Jessica"),
        ("p", "show_tab('paul')", "Paul"),
        ("q", "quit", "Quit"),
    ]

    CSS = """
        .shell_util {
            min-height: 5;
        }

        #progress-bar {

            dock: bottom;
            margin: 1;
            background: dodgerblue;

        }
    """

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""

        # Add the TabbedContent widget
        with TabbedContent(initial="shell-utils") as tc:
            with TabPane("SHELL UTILS", id="shell-utils"):  # First tab
                
                for shellutil in SHELLUTILS:
                    yield Horizontal(
                            Switch(value=shellutil['is_active'], classes="shell-util", id=f"shellutil-{shellutil['id']}"),
                            Markdown(f"__{shellutil['name']}__\n\n{shellutil['description']}"),
                            classes="shell_util",
                                )
            with TabPane("PACKAGES", id="packages"):
                
                for package in PACKAGES:
                    yield Horizontal(
                            Switch(value=package['is_installed'], classes="packages", id=f"package-{package['id']}"),
                            Markdown(f"__{package['name']}__\n\n{package['description']}"),
                            classes="shell_util",
                                )
            with TabPane("Jessica", id="jessica"):
                yield Markdown(JESSICA)
                with TabbedContent("Paul", "Alia"):
                    yield TabPane("Paul", Label("First child"))
                    yield TabPane("Alia", Label("Second child"))

            with TabPane("Paul", id="paul"):
                yield Markdown(PAUL)

        # Footer to show keys
        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab

    async def on_switch_changed(self, event: Switch.Changed) -> None:
        """Handle switch state change."""
        switch = event.switch
        switch_id = switch.id

        # :/SHELL UTILS
        if switch_id.startswith('shellutil-'):
            shellutil_id = switch_id.replace('shellutil-', '')
            shellutils_toggle(shellutil_id)

def run_sysconfig():
    app = TabbedApp()
    app.run()
