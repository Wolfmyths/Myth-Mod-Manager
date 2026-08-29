import os

import pytest

from PySide6.QtCore import QMutex

from src.helpers.save_manager import Save
from src.objects.delete_mod import DeleteMod

MOCK_MODS = (
    ('make game easy mod', True), 
    ('best mod ever', False),
    ('super fun mod', True)
)

@pytest.mark.parametrize(("mod_name", "disabled"), MOCK_MODS)
def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str, mod_name: str, disabled: bool) -> None:  # pyright: ignore[reportUnusedParameter]
    Save.setEnabled(mod_name, disabled)
    mutex = QMutex()
    worker = DeleteMod('make game easy mod')
    worker.mutex = mutex

    worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) is False
    assert os.path.isdir(create_mod_dirs)

    worker.deleteLater()
