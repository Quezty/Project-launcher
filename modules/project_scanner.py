from os import scandir
from dataclasses import dataclass
import yaml

@dataclass
class DirectoryInfo:
    name: str
    path: str
    markdown: str

PROJECT_DIRECTORY = "/home/joachims/repos"

def grab_project_info(directory: str) -> list[DirectoryInfo]:
    """ Grabs readme information for all projects in given directory

    Args:
        directory(str): root directory for projects

    Returns:
        list: Returns a list of DirectoryInfo objects, accessible through list_name[index].name/path/markdown

    """

    objects = []

    with scandir(directory) as root_dir:
        for entry in root_dir:
            if not entry.name.startswith('.') and entry.is_dir():
                current_project_directory = directory + "/" + entry.name
                with scandir(current_project_directory) as subdir:
                    for file in subdir:
                        if file.name in ("README.md", "readme.md"):
                            readme_file_path = current_project_directory + "/" + file.name
                            with open(readme_file_path, "r", encoding="utf-8") as md_file:
                                markdown_content = md_file.read()

                            project_info = DirectoryInfo(entry.name, current_project_directory, markdown_content)
                            objects.append(project_info)
    return objects

def init_projects_config(directory: str, filename: str) -> None:

    """ Grab readme, path and name for all projects in input directory

    Args:
        directory(str): projects folder 
        filename(str): Name/path of configuration file
    """


    project_data = {
            'Projects': [ ]
            }

    with scandir(directory) as root_dir:
        for entry in root_dir:
            if not entry.name.startswith('.') and entry.is_dir():
                current_project_directory = directory + "/" + entry.name
                with scandir(current_project_directory) as subdir:
                    for file in subdir:
                        if file.name in ("README.md", "readme.md"):
                            readme_file_path = current_project_directory + "/" + file.name

                            project_data['Projects'].append({
                                "name": entry.name,
                                "path": current_project_directory,
                                "readme_path": readme_file_path
                                })

    with open(file=filename, mode='w', encoding='utf-8') as file:
        yaml.dump(project_data, file)

def grab_projects(filename) -> dict:
    project_data = {}

    with open(file=filename, mode='r', encoding='utf-8') as file:
        project_data = yaml.safe_load(file)

    return project_data



# uncomment line underneath to print the data
# print(grab_project_info(PROJECT_DIRECTORY))

# grab_projects("testing.yaml")

# init_projects_config(PROJECT_DIRECTORY, "config.yaml")
