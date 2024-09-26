# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/sysconfig.py]
# :author        : fantomH
# :created       : 2024-09-06 15:27:10 UTC
# :updated       : 2024-09-10 11:54:26 UTC
# :description   : cli.

from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Markdown, TabbedContent, TabPane
from textual.containers import Horizontal
from textual.widgets import Static, Switch

# from database import shell_utils_toggle
# from database import shell_utils_requirements
# from shellutils import install_shell_util

from shellutils import shellutils_to_listdicts
from shellutils import shellutils_toggle

SHELLUTILS = shellutils_to_listdicts()

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
    """

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        yield Footer()

        # Add the TabbedContent widget
        with TabbedContent(initial="shell-utils") as tc:
            with TabPane("SHELL UTILS", id="shell-utils"):  # First tab
                
                for shellutil in SHELLUTILS:
                    yield Horizontal(
                            Switch(value=shellutil['is_active'], classes="shell-util", id=f"shellutil-{shellutil['id']}"),
                            Markdown(f"__{shellutil['name']}__\n\n{shellutil['description']}"),
                            classes="shell_util",
                                )
            with TabPane("Jessica", id="jessica"):
                yield Markdown(JESSICA)
                with TabbedContent("Paul", "Alia"):
                    yield TabPane("Paul", Label("First child"))
                    yield TabPane("Alia", Label("Second child"))

            with TabPane("Paul", id="paul"):
                yield Markdown(PAUL)

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
            # shell_utils_requirements(shell_util_id)
            # install_shell_util(shell_util_id)

def run_sysconfig():
    app = TabbedApp()
    app.run()
