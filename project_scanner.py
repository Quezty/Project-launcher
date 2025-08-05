import os
from dataclasses import dataclass

@dataclass
class DirectoryInfo:
    name: str
    path: str
    markdown: str

PROJECT_DIRECTORY = "/home/codespace/repos"

def grab_project_info(directory: str) -> list[DirectoryInfo]:
    """ Grabs readme information for all projects in given directory

    Args:
        directory(str): root directory for projects

    Returns:
        list: Returns a list of DirectoryInfo objects, accessible through list_name[index].name/path/markdown

    """

    objects = []

    with os.scandir(directory) as root_dir:
        for entry in root_dir:
            if not entry.name.startswith('.') and entry.is_dir():
                current_project_directory = directory + "/" + entry.name
                with os.scandir(current_project_directory) as subdir:
                    for file in subdir:
                        if file.name in ("README.md", "readme.md"):
                            readme_file_path = current_project_directory + "/" + file.name
                            with open(readme_file_path, "r", encoding="utf-8") as md_file:
                                markdown_content = md_file.read()

                            project_info = DirectoryInfo(entry.name, current_project_directory, markdown_content)
                            objects.append(project_info)
    return objects
