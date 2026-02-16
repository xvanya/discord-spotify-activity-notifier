@echo off
REM Activate virtual environment if you have one
REM Otherwise, just run python directly

REM Go to the project directory
cd /d "%~dp0"

REM Run the bot
python ActivityBot.py

pause
