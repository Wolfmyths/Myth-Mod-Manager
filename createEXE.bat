@echo on

echo Installing Dependencies
pip install -r requirements.txt

echo Running Pyinstaller...
pyinstaller --clean main.spec --distpath ./

echo Deleting Build Folder
rmdir /s /q build