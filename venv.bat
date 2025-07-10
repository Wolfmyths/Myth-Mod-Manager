set "ROOT=."

if not exist "%ROOT%\venv" (
	py -m venv "%ROOT%\venv"
)
	
cd "%ROOT%\venv\Scripts"
activate