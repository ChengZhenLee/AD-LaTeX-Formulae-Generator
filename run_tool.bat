@echo off
REM Launcher for native Windows shells (cmd.exe / PowerShell).
REM For Linux, macOS, WSL, or Git Bash use run_tool.sh instead.

REM Prefer the `py` launcher (installed alongside python.org builds),
REM falling back to `python` on the PATH.
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    py -3 main.py
    goto :eof
)

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    python main.py
    goto :eof
)

echo Error: Python 3 is not installed. Please install it to continue.
exit /b 1
