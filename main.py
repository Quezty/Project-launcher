from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Input, Label, Static
from textual.containers import Horizontal

class ProjectLauncher(App):

    CSS_PATH = "styles.tcss"
    TITLE = "Project Launcher"
    SUB_TITLE = "A TUI project launcher and project manager"
    THEME = "Tokyo Night"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input()
        yield Horizontal(
            ListView(
                ListItem(Label("One")),
                ListItem(Label("Two")),
                ListItem(Label("Three"))
            ),
            Static("test")
        )
        yield Footer()

if __name__ == "__main__":
    app = ProjectLauncher()
    app.run()
