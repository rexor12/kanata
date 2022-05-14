@echo off
REM Run this script while standing in the project's root directory to create packages.
REM Note: It requires having "python" in the PATH environment variable.
setlocal
echo Upgrading 'build'...
python -m pip install --upgrade build
echo 'build' upgraded.

echo Building package...
cd /D "%CD%"
python -m build
echo Build complete.