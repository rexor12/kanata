@echo off
REM Run this script while standing in the project's root directory to execute tests.
REM Note: It requires having "python" in the PATH environment variable.
REM To be able to successfully run and edit tests, make sure you install
REM the library in editable mode first:
REM python -m pip install -e .
setlocal
echo Running tests..
cd /D "%CD%"
python -m pip install -U coverage
coverage run -m unittest -v
coverage xml
echo Running tests complete.
