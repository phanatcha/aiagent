# AI Agent

AI Agent is a command-line assistant for automated code debugging and lightweight refactoring. It iteratively plans and executes actions—scanning files, reading/writing source code, and running Python—to work toward a user-defined task. The agent uses Google’s Gemini API for reasoning and planning.

---

## 🚀 Features

* Repository scanning with include/exclude globs
* Read and analyze file contents
* Safe in-place edits with dry-run previews and edit limits
* Execute Python files/commands to validate changes
* Iterative loop with step and edit safety caps
* JSON/text output for CLI and CI use

---

## 🧠 Requirements
* Python 3.10+
* macOS, Linux, or Windows (PowerShell or WSL)
* Gemini API key (`GEMINI_API_KEY`)

---

## 📦 Installation

```bash
# Clone
git clone https://github.com/phanatcha/aiagent.git
cd aiagent

# Create & activate a virtual environment
python3 -m venv .venv

# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install dependencies
# If your repo has pyproject.toml/setup.cfg:
pip install -e .
# Or, if you maintain requirements.txt:
pip install -r requirements.txt
```

---

## 🛠️ Configuration
Create a .env file at the repository root:

```bash
GEMINI_API_KEY=your_key_here
```
(Optional) Persist defaults in `aiagent.toml`:

```toml
[paths]
root = "."
include = ["**/*.py"]
exclude = ["**/.venv/**", "**/__pycache__/**", "**/build/**"]

[safety]
max_steps = 20
max_edits = 25
dry_run_default = true
```
> CLI flags always override config.

---

## 📍 Usage
### Quick start

```bash
# Analyze without modifying files
python3 main.py "explain why tests fail" --dry-run

# Plan → edit → verify
python3 main.py "fix failing tests in src/ and run pytest" \
  -r . --include '**/*.py'

```
### CLI reference
```sql
python3 main.py <task> [options]

Positional:
  task                      Natural-language instruction for the agent

Options:
  -r, --root PATH           Project root (default: .)
      --include GLOB        Repeatable; files to include (e.g., --include '**/*.py')
      --exclude GLOB        Repeatable; files/dirs to exclude
      --max-steps INT       Maximum tool calls per task (default: 20)
      --max-edits INT       Maximum files allowed to change (default: 25)
      --dry-run             Show planned edits; do not write
      --json                Emit JSON output
      --verbose, -v         Increase logging verbosity

```
### Tooling primitives (built-ins)
* `get_files_info` - enumerate files (honors include/exclude)
* `get_file_content` - read file text
* `write_file` - apply edits with safeguards
* `run_python_file` - execute `python <path>` and capture output
The agent selects among these in a loop until the goal is achieved or limits are reached.

---

## 🎲 Examples

```bash
# Focused analysis of one module
python3 main.py "find the bug in src/calc.py and propose a patch" --dry-run

# Apply straightforward fixes and commit later yourself
python3 main.py "resolve import errors across src/" --include '**/*.py'

# Reproduce + verify
python3 main.py "run tests and fix simple failures"
```

---

## 🧩 Code Structure

```bash
├── README.md
├── __pycache__/
├── calculator
│   ├── README.md
│   ├── lorem.txt
│   ├── main.py
│   ├── pkg
│   └── tests.py
├── call_function.py
├── config.py
├── functions
│   ├── __pycache__
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python.py
│   └── write_file.py
├── main.py
├── prompts.py
├── requirements.txt
├── tests.py
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg
```

---

## Troubleshooting
* **Auth errors** → verify `GEMINI_API_KEY` and that `.env` is loaded (e.g., via `python-dotenv`)
* **No edits applied** → remove `--dry-run`, loosen `--exclude`, or increase `--max-edits`
* **Agent loops** → reduce `--max-steps`, narrow the task, or target a single module

---
