import os

PROJECT_DIRECTORY = "/home/codespace/repos"

with os.scandir(PROJECT_DIRECTORY) as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir():
            current_project_directory = PROJECT_DIRECTORY + "/" + entry.name
            with os.scandir(current_project_directory) as list:
                for file in list:
                    if file.name == "readme.md" or file.name == "README.md":
                        readme_file_path = current_project_directory + "/" + file.name
                        with open(readme_file_path, "r", encoding="utf-8") as md_file:
                            markdown_content = md_file.read()
                        print(markdown_content) 