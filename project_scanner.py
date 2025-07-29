import os

PROJECT_DIRECTORY = "~/repos"

with os.scandir("/") as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir():
            print(entry.name)