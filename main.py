from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Input, Label, Static
from textual.containers import Horizontal
from textual.events import Key
from project_scanner import grab_project_info

PROJECT_ROOT_DIRECTORY = "/home/codespace/repos"

class ProjectLauncher(App):

    CSS_PATH = "styles.tcss"
    TITLE = "Project Launcher"
    SUB_TITLE = "A TUI project launcher and project manager"
    THEME = "Tokyo Night"

    BINDINGS = [
        ("q", "quit", "quit the app"),
        ("s", "focus_searchbar", "search")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(id="Searchbar")
        yield Horizontal(
            ListView(
                ListItem(Label("One")),
                ListItem(Label("Two")),
                ListItem(Label("Three")),
                id="ProjectList"
            ),
            Static("test")
        )
        yield Footer()
    
    def on_mount(self) -> None:
        PROJECTS = grab_project_info(PROJECT_ROOT_DIRECTORY)
        self.searchbar = self.query_one("#Searchbar", Input)
        self.list = self.query_one("#ProjectList", ListView)
        self.set_focus(self.list)

    def on_key(self, event: Key) -> None:
        if self.focused == self.list:
            if event.key == "j":
                self.list.index = min(self.list.index + 1, len(self.list.children) - 1)
                event.stop()
            elif event.key == "k":
                self.list.index = max(self.list.index - 1, 0)
                event.stop()
        
        if self.focused == self.searchbar:
            if event.key == "escape":
                self.set_focus(self.list)

    def action_focus_searchbar(self) -> None:
        self.set_focus(self.searchbar)


if __name__ == "__main__":
    app = ProjectLauncher()
    app.run()
