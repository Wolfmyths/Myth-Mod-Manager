from collections.abc import Generator
import os
import platform
import shutil

import pytest
from pytestqt.qtbot import QtBot

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

@pytest.fixture
def deletemod(createTemp_Mod_ini: str) -> Generator[DeleteMod]:
    deletemod = DeleteMod()

    Save(createTemp_Mod_ini)

    yield deletemod

    deletemod.deleteLater()

    Save.clearModData()
    Save._path = ''  # pyright: ignore[reportPrivateUsage]

@pytest.mark.parametrize(("mod_name", "disabled"), MOCK_MODS)
def test_deletemod(qtbot: QtBot, deletemod: DeleteMod, monkeypatch: pytest.MonkeyPatch, create_mod_dirs: str, createTemp_Config_ini: str, mod_name: str, disabled: bool) -> None:  # pyright: ignore[reportUnusedParameter]
    if platform.system().startswith("Linux"):
        # QFile.moveToTrash doesn't work on tmp files on Linux
        monkeypatch.setattr("src.objects.delete_mod.QFile", Mock_QFile)

    Save.setEnabled(mod_name, disabled)

    deletemod.mods = ('make game easy mod', )

    with qtbot.wait_signal(deletemod.succeeded, timeout=500):
        deletemod.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) is False
    assert os.path.isdir(create_mod_dirs)
