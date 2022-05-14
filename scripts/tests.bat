@echo off
REM Run this script while standing in the project's root directory to execute tests.
REM Note: It requires having "python" in the PATH environment variable.
setlocal
echo Running tests..
cd /D "%CD%"
python -m unittest -v
echo Running tests complete.