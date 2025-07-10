echo Setting Variables
ROOT="../"
disFolder="Myth Mod Manager"
Exe="Myth Mod Manager.exe"
Txt="requirements.txt"
Spec="main.spec"

echo Installing Dependencies
pip install -r "${ROOT}${Txt}"

echo Running Pyinstaller
pyinstaller --clean "${ROOT}${Spec}" --distpath "${ROOT}${disFolder}"

echo Installation Finished!