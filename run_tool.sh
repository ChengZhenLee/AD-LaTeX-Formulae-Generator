#!/usr/bin/env bash
# Launcher for Unix-like shells: Linux, macOS, WSL, and Git Bash on Windows.
# For native Windows (cmd.exe / PowerShell) use run_tool.bat instead.

# Prefer `python3`, but fall back to `python` since some environments
# (notably plain Python installs on Windows) only provide the latter.
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python 3 is not installed. Please install it to continue." >&2
    exit 1
fi

"$PYTHON" main.py