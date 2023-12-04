@echo off

if not exist requirements.txt (
    echo requirements.txt file not found.
    pause
    exit /b
)

pip install -r requirements.txt

pause