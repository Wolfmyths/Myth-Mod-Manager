@echo on

echo Setting Variables
set "disFolder=Myth Mod Manager"
set "Exe=Myth Mod Manager.exe"
set "Txt=requirements.txt"
set "Spec=main.spec"
set "ROOT=."

echo Installing Dependencies
pip install -r "%ROOT%\%Txt%"

echo Running Pyinstaller
pyinstaller --clean "%ROOT%\%Spec%" --distpath "%ROOT%\%disFolder%"

echo Installation Finished!
pause