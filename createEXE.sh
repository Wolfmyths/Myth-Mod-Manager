echo Setting Variables
disFolder="Myth Mod Manager"
Exe="Myth Mod Manager.exe"
Txt="requirements.txt"
Spec="main.spec"

echo Installing Dependencies
pip install -r "${Txt}"

echo Running Pyinstaller
pyinstaller --clean "${Spec}" --distpath "${disFolder}"

echo Installation Finished!