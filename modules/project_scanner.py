import os
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

def grab_project_info_yaml(directory: str):
    with os.scandir(directory) as root_dir:
        for entry in root_dir:
            if not entry.name.startswith('.') and entry.is_dir():
                current_project_directory = directory + "/" + entry.name
                print()



data = {
        'Projects': [
            {'name': 'test', 'path': 'somelpath'},
            {'name': 'test2', 'path': 'anotherpath'}
        ]
}

yaml_output = yaml.dump(data, default_flow_style=False)

with open('projects.yaml', 'w') as f:
    yaml.dump(data, f, sort_keys=False)
    f.close()

with open('projects.yaml', 'r') as f:
    data = yaml.safe_load(f)
    output = dict(data)
    print(output['Projects'][0])

print(yaml_output)

# grab_project_info_yaml(PROJECT_DIRECTORY)

# uncomment line underneath to print the data
# print(grab_project_info(PROJECT_DIRECTORY))
