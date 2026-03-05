# Contributing

Thanks for your interest in improving this project.

## Setup

1. Fork and clone the repository.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows (PowerShell)
.\\.venv\\Scripts\\Activate.ps1
# macOS/Linux
# source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Run tests from the same venv:

```bash
python -m pytest -q
```

## Development Guidelines

- Keep changes focused and small.
- Add or update tests for behavior changes.
- Prefer clear function names and docstrings for non-trivial logic.
- Run tests locally before opening a PR.

## Pull Request Checklist

- Code builds and tests pass.
- New behavior has tests.
- README/docs are updated if interfaces changed.
- PR description explains what changed and why.

## Reporting Issues

Please include:
- Expected behavior
- Actual behavior
- Reproduction steps
- Environment details (OS, Python version, GPU/CPU)
