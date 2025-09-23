from os import scandir
from dataclasses import dataclass
import yaml

@dataclass
class DirectoryInfo:
    name: str
    path: str
    markdown: str

PROJECT_DIRECTORY = "/home/joachims/repos"


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
# Yes this is my debugging skills so far......
# grab_projects("testing.yaml")

# init_projects_config(PROJECT_DIRECTORY, "config.yaml")
