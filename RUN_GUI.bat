@echo off
rem set to this directory
set PROGRAM_DIR=%~dp0

set

set PROGRAM_DIR=%PROGRAM_DIR:\\=\%
echo. & echo PROGRAM_DIR home is %PROGRAM_DIR% & echo.

set PATH=%PATH%;C:/PYTHON27

python ./gui_layer/gui.py

@echo on