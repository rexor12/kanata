@echo off
setlocal
echo Upgrading twine...
python -m pip install --upgrade twine
echo Upgraded twine.

cd /D "%CD%"
echo Uploading to pypi...
python -m twine upload dist/*
echo Upload complete.