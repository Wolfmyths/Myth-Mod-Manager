import os
import platform
import shutil

import pytest

from src.helpers.save_manager import Save
from src.objects.delete_mod import DeleteMod

class Mock_QFile:
    def __init__(self, path: str) -> None:
        self.path = path
        #print("Mock QFile Created with the path:", path)
    
    def moveToTrash(self) -> bool:
        #print("Moving to trash")
        shutil.rmtree(self.path)
        return not os.path.exists(self.path)
    
    def errorString(self) -> str:
        return "Mock error string"
    
    def error(self) -> str:
        return "Mock error"

MOCK_MODS = (
    ('make game easy mod', True), 
    ('best mod ever', False),
    ('super fun mod', True)
)

@pytest.mark.parametrize(("mod_name", "disabled"), MOCK_MODS)
def test_thread(monkeypatch: pytest.MonkeyPatch, create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str, mod_name: str, disabled: bool) -> None:  # pyright: ignore[reportUnusedParameter]
    if platform.system().startswith("Linux"):
        # QFile.moveToTrash doesn't work on tmp files on Linux
        monkeypatch.setattr("src.objects.delete_mod.QFile", Mock_QFile)

    Save(createTemp_Mod_ini)
    Save.setEnabled(mod_name, disabled)

    worker = DeleteMod('make game easy mod')
    worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) is False
    assert os.path.isdir(create_mod_dirs)

    worker.deleteLater()

    Save.clearModData()
    Save._path = ''  # pyright: ignore[reportPrivateUsage]
