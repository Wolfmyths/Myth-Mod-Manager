@echo on

echo Setting Variables
set disFolder="Myth Mod Manager"
set Exe="Myth Mod Manager.exe"
set Txt="requirements.txt"
set Spec="main.spec"

echo Installing Dependencies
pip install -r %Txt%

echo Installing Pyinstaller
pip install pyinstaller

echo Running Pyinstaller
pyinstaller --clean %Spec% --distpath ./%disFolder%

echo Installation Finished!