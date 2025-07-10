ROOT="."

if [ ! -d "${ROOT}/venv"]; then
	python -m venv "${ROOT}/venv"
fi
	
cd "${ROOT}/venv/bin"
activate