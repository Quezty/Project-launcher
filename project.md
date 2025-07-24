# Project Launcher TUI Plan

This document outlines the plan for building a Textual-based Project Launcher TUI.

---

## **Goal**
Create a terminal user interface (TUI) to:
- Display a list of projects (auto-discovered from a folder).
- Show descriptions and actions for the selected project.
- Provide a search bar for quick filtering.
- Allow keybind-based actions (e.g., open in terminal, run tests, open editor).
- Integrate with a shell wrapper to `cd` into projects.

---

## **Project Structure**
```
project-launcher/
│
├── main.py            # Entry point of the TUI app.
├── project_scanner.py # Logic for scanning directories and gathering project info.
├── actions.py         # Functions for project-specific actions (tests, start server, etc.).
├── ui/                # UI-specific components.
│   ├── __init__.py
│   ├── views.py       # Layout (search bar, list, description pane).
│   └── widgets.py     # Custom widgets (list, description box).
└── project.md         # This planning file.
```

---

## **Step-by-Step Plan**

### **Step 1: Setup**
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install textual rich
   ```
2. Create the folder structure above.

---

### **Step 2: Layout Design**
- **Top row:** Search bar (`Input` widget).
- **Left pane:** Project list (`ListView`).
- **Right pane:** Project details (`Static` or `Markdown` widget).
- **Bottom bar:** Footer with keybind hints.

---

### **Step 3: Project Model**
- Use a `Project` class or dictionary:
  ```python
  {
    "name": "CLI Tool",
    "path": "/home/user/projects/cli-tool",
    "description": "A small CLI utility for X",
    "commands": ["test", "start", "open"]
  }
  ```
- `project_scanner.py` will:
  - Scan `~/projects` (or configurable folder).
  - Read `README.md` or `.projectinfo` for descriptions.
  - Return a list of `Project` objects.

---

### **Step 4: Search Filtering**
- Listen to search bar `on_change`.
- Filter `ListView` items dynamically.
- Keep track of which project is currently highlighted.

---

### **Step 5: Keybinds**
- Define `BINDINGS` in `main.py`:
  - `j/k` or arrow keys → Navigate projects.
  - `Enter` → Default action (e.g., print `CD:<path>`).
  - `T` → Run tests.
  - `E` → Open editor (`nvim`).
  - `Q` → Quit.

---

### **Step 6: Project Details Panel**
- When selection changes:
  - Update description pane.
  - Display available commands.

---

### **Step 7: Actions**
- `actions.py` contains async functions:
  - `run_tests(project_path)`
  - `start_server(project_path)`
  - `open_editor(project_path)`
- Use `asyncio.create_subprocess_exec` to run commands and display output.

---

### **Step 8: Shell Wrapper Integration**
- The TUI exits with `print(f"CD:{project_path}")` when the user chooses "enter project."
- A shell function (in `~/.bashrc`):
  ```bash
  proj() {
    local out
    out="$(python3 ~/project-launcher/main.py)" || return
    case "$out" in
      CD:*)
        cd "${out#CD:}"
        ;;
    esac
  }
  ```

---

### **Step 9: Polish**
- Add colors, icons (emoji), and styles.
- Use Markdown for nicer description formatting.
- Add a status bar (keybind hints).

---

### **Step 10: Future Enhancements**
- Preview README.md or other files inline.
- Async background tasks (e.g., run tests while browsing other projects).
- Git integration (show branch/uncommitted changes).
- Configuration file for commands and layout.

---
