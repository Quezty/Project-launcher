from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Input, Label, Markdown 
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.message import Message
from modules.project_scanner import grab_project_info

PROJECT_ROOT_DIRECTORY = "/home/codespace/repos"

class ProjectSearchbar(Input):
    """Input field with logic to unblur and clear itself"""

    BINDINGS = [
        ("ctrl+s", "blur_and_move_focus", "move to list"),
        ("ctrl+d", "clear_search", "Clear searchbar")
    ]

    def __init__(self) -> None:
        super().__init__()
        self.value = ""

    class BlurRequested(Message):
        def __init__(self, sender: "ProjectSearchbar") -> None:
            super().__init__()
            self.sender = sender

    def update_value(self) -> None:
        self.value = ""


    def action_blur_and_move_focus(self) -> None:
        """Sends blur message to App class"""
        self.post_message(self.BlurRequested(self))

    def action_clear_search(self) -> None:
        """Clears searchbar"""
        self.value = ""


class ProjectLauncher(App):
    """Main app class"""

    CSS_PATH = "styles.tcss"
    THEME = "Tokyo Night"

    BINDINGS = [
        ("q", "quit", "quit the app"),
        ("s", "focus_searchbar", "search"),
        ("k", "move_up", "move up"),
        ("j", "move_down", "move down"),
        ("ctrl+d", "clear_search", "Clear searchbar"),
        ("enter", "choose_project", "Open project")
    ]

    selected_index = reactive(0)

    def __init__(self):
        super().__init__()
        self.PROJECTS = []
        self.filtered_projects = []



    def compose(self) -> ComposeResult:
        yield ProjectSearchbar()
        yield Horizontal(
            ListView(
                id="ProjectList"
            ),
            Markdown(
                "Loading...",
                id="MarkdownViewer"
            )
        )
        yield Footer()

    async def on_mount(self) -> None:
        self.PROJECTS = grab_project_info(PROJECT_ROOT_DIRECTORY)
        self.searchbar = self.query_one(ProjectSearchbar)
        self.list = self.query_one("#ProjectList", ListView)
        self.list.border_title = f"Projects - {PROJECT_ROOT_DIRECTORY}"
        self.markdown = self.query_one("#MarkdownViewer", Markdown)
        self.markdown.border_title = f"README.md - {self.PROJECTS[0].path}"
        
        for project in self.PROJECTS:
            await self.list.append(ListItem(Label(project.name)))

        self.markdown.update(self.PROJECTS[0].markdown)

        self.list.index = 0
        self.set_focus(self.list)


    def action_move_down(self) -> None:
        """Moves cursor 1 item down"""
        self.selected_index = self.selected_index + 1 if self.selected_index < len(self.list.children) - 1 else self.selected_index

    def action_move_up(self) -> None:
        """Moves cursor 1 item up"""
        self.selected_index = self.selected_index - 1 if self.selected_index != 0  else self.selected_index

    def action_focus_searchbar(self) -> None:
        """Focuses searchbar"""
        self.set_focus(self.searchbar)

    def action_clear_search(self) -> None:
        """Clears searchbar"""
        self.searchbar.update_value()

    async def on_input_changed(self, event: Input.Changed) -> None:
        filter = event.value
        self.list.clear()
        self.markdown.update("searching...")
        self.filtered_projects = self.project_filter(self.PROJECTS, filter)

        for project in self.filtered_projects:
            await self.list.append(ListItem(Label(project.name)))

        try:
            self.markdown.update(self.filtered_projects[0].markdown)
        except IndexError:
            self.markdown.update(f"No project found matching string {filter}!")


    def on_project_searchbar_blur_requested(self, event: ProjectSearchbar.BlurRequested) -> None:
        self.set_focus(self.list)
        self.selected_index = 0
        self.list.index = 0


    def watch_selected_index(self, value: int) -> None:
        self.list.index = value
        if not self.filtered_projects:
            self.markdown.update(self.PROJECTS[value].markdown)
            self.markdown.border_title = f"README.md - {self.PROJECTS[value].path}"
        else:
            self.markdown.update(self.filtered_projects[value].markdown)
            self.markdown.border_title = f"README.md - {self.filtered_projects[value].path}"


    def project_filter(self, project_list: list, filter: str) -> list:
        filtered_list = []

        for entry in project_list:
            if filter.lower() in entry.name.lower():
                filtered_list.append(entry)


        return filtered_list

if __name__ == "__main__":
    app = ProjectLauncher()
    app.run()
