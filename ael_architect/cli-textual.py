# :----------------------------------------------------------------------- INFO
# :[ael-architect/ael_architect/cli.py]
# :author        : fantomH
# :created       : 2024-09-06 15:27:10 UTC
# :updated       : 2024-09-10 11:54:26 UTC
# :description   : cli.

from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, Markdown, TabbedContent, TabPane
from textual.containers import Horizontal
from textual.widgets import Static, Switch

from database import shell_utils_to_dictionaries
from database import shell_utils_toggle
from database import shell_utils_requirements
from shell_utils import install_shell_util

SHELL_UTILS = shell_utils_to_dictionaries()

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
                
                for shell_util in SHELL_UTILS:
                    yield Horizontal(
                            Switch(value=shell_util['is_active'], classes="shell-util", id=f"shell_util-{shell_util['id']}"),
                            Markdown(f"__{shell_util['name']}__\n\n{shell_util['description']}"),
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

        # :SHELL UTILS
        if switch_id.startswith('shell_util-'):
            shell_util_id = switch_id.replace('shell_util-', '')
            shell_utils_toggle(shell_util_id)
            shell_utils_requirements(shell_util_id)
            install_shell_util(shell_util_id)

if __name__ == "__main__":
    app = TabbedApp()
    app.run()
