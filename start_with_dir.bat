@echo off
REM Claude Code launcher with custom working directory
REM Usage: start_with_dir.bat <target-directory> [additional args...]

if "%~1"=="" (
    echo Usage: start_with_dir.bat ^<directory^> [args...]
    echo Example: start_with_dir.bat C:\my-project
    exit /b 1
)

REM Claude Code project root (where this script lives)
set "CLAUDE_DIR=%~dp0%"

set "TARGET_DIR=%~1"
shift

if not exist "%TARGET_DIR%" (
    echo Error: Directory "%TARGET_DIR%" does not exist
    exit /b 1
)

REM Pass target directory to the code via env var
set "CLAUDE_CODE_OVERRIDE_CWD=%TARGET_DIR%"

REM Always run from project root so bun finds package.json & node_modules
cd /d "%CLAUDE_DIR%"
bun run dev --dangerously-skip-permissions %*