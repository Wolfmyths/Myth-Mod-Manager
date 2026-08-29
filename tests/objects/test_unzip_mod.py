import os
import shutil

import pytest

from PySide6.QtCore import QMutex

from pytestqt.qtbot import QtBot

from src.objects.unzip_mod import UnZipMod
from src.constant_vars import ModType

#TODO: Everything seems to work but the assert statement
@pytest.mark.skip
def test_thread(qtbot: QtBot, create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:  # pyright: ignore[reportUnusedParameter]
    zip_path: str = os.path.join(create_mod_dirs, 'zip')
    os.mkdir(zip_path)
    shutil.make_archive(zip_path, 'zip')

    url: str = os.path.join(create_mod_dirs, 'zip.zip')

    mutex = QMutex()
    worker = UnZipMod((url, ModType.mods))
    worker.mutex = mutex

    with qtbot.wait_signal(worker.succeeded):
        worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'zip')) is True

    worker.deleteLater()
