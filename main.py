from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Input, Label, Markdown
from textual.containers import Horizontal
from textual.events import Key
from textual.reactive import reactive
from textual.message import Message
from project_scanner import grab_project_info

PROJECT_ROOT_DIRECTORY = "/home/codespace/repos"

class ProjectSearchbar(Input):

    BINDINGS = [
        ("ctrl+s", "blur_and_move_focus", "move to list"),
        ("ctrl+d", "clear_search", "Clear searchbar")        
    ]

    class BlurRequested(Message):
        def __init__(self, sender: "ProjectSearchbar") -> None:
            super().__init__()
            self.sender = sender

    def action_blur_and_move_focus(self) -> None:
        self.post_message(self.BlurRequested(self))

    def action_clear_search(self) -> None:
        self.value = ""


class ProjectLauncher(App):

    CSS_PATH = "styles.tcss"
    TITLE = "Project Launcher"
    SUB_TITLE = "A TUI project launcher and project manager"
    THEME = "Tokyo Night"

    BINDINGS = [
        ("q", "quit", "quit the app"),
        ("s", "focus_searchbar", "search"),
        ("k", "move_up", "move up"),
        ("j", "move_down", "move down")
    ]

    selected_index = reactive(0)

    def __init__(self):
        super().__init__()
        self.PROJECTS = []
        self.project_index = 0



    def compose(self) -> ComposeResult:
        yield Header()
        yield ProjectSearchbar(id="Searchbar")
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
        self.searchbar = self.query_one("#Searchbar", ProjectSearchbar)
        self.list = self.query_one("#ProjectList", ListView)
        self.markdown = self.query_one("#MarkdownViewer", Markdown)

        for project in self.PROJECTS:
            await self.list.append(ListItem(Label(project.name)))

        self.markdown.update(self.PROJECTS[0].markdown)

        self.list.index = 0
        self.set_focus(self.list)

    
    def action_move_down(self) -> None:
        self.selected_index = self.selected_index + 1 if self.selected_index < len(self.list.children) - 1 else self.selected_index

    def action_move_up(self) -> None:
        self.selected_index = self.selected_index - 1 if self.selected_index != 0  else self.selected_index

    def action_focus_searchbar(self) -> None:
        self.set_focus(self.searchbar)

    async def on_input_changed(self, event: Input.Changed) -> None:
        filter = event.value
        self.list.clear()
        self.markdown.update("searching...")
        filtered_projects = self.project_filter(self.PROJECTS, filter)

        for project in filtered_projects:
            await self.list.append(ListItem(Label(project.name))) 

        try:
            self.markdown.update(filtered_projects[0].markdown)
        except:
            self.markdown.update("No project selected/found")
        

    def on_project_searchbar_blur_requested(self, event: ProjectSearchbar.BlurRequested) -> None:
        self.set_focus(self.list)
        
    
    def watch_selected_index(self, value: int) -> None:
        self.list.index = value 
        self.project_index = value
        self.markdown.update(self.PROJECTS[value].markdown)

    def project_filter(self, project_list: list, filter: str) -> list:
        filtered_list = []

        for entry in project_list:
            if filter.lower() in entry.name.lower():
                filtered_list.append(entry)


        return filtered_list

if __name__ == "__main__":
    app = ProjectLauncher()
    app.run()
