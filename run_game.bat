@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
if errorlevel 1 pause
py game.py
if errorlevel 1 pause
