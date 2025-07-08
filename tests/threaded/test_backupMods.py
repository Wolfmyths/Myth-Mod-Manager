import os
import shutil

import pytest

from PySide6.QtCore import QMutex

from src.threaded.backupMods import BackupMods
from src.constant_vars import BACKUP_MODS

#TODO: os.mkdir() isn't working
@pytest.mark.skip
def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    mutex = QMutex()
    worker = BackupMods()
    
    bundledFilePath: str = os.path.join(create_mod_dirs, BACKUP_MODS)
    worker.bundledFilePath = bundledFilePath
    worker.mutex = mutex

    worker.start()

    assert os.path.isfile(f'{bundledFilePath}.zip')

    shutil.unpack_archive(f'{bundledFilePath}.zip', create_mod_dirs)

    assert os.listdir(bundledFilePath) == ['mods', 'assets', 'Maps']
    assert os.listdir(os.path.join(bundledFilePath, 'mods')) == ['make game easy mod']
    assert os.listdir(os.path.join(bundledFilePath, 'assets', 'mod_overrides')) == ['best mod ever']
    assert os.listdir(os.path.join(bundledFilePath, 'Maps')) == ['super fun mod']
