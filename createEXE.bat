@echo on

echo Setting Variables
set Exe="Myth Mod Manager.exe"
set Txt="requirements.txt"
set Spec="main.spec"

echo Installing Dependencies
pip install -r %Txt%

echo Running Pyinstaller
pyinstaller --clean %Spec% --distpath ./

echo Opening Exe
%Exe%