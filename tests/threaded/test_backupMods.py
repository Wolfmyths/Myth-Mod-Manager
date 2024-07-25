import os
import shutil

import pytest

from src.threaded.backupMods import BackupMods
from src.getPath import Pathing
from src.save import OptionsManager, Save
from src.constant_vars import BACKUP_MODS

#TODO: os.mkdir() isn't working
@pytest.mark.skip
def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    dispath = os.path.join(create_mod_dirs, 'disabledMods')
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.setDispath(dispath)
    parser.writeData()

    worker = BackupMods()
    worker.saveManager = Save(createTemp_Mod_ini)
    worker.optionsManager = parser
    bundledFilePath = os.path.join(create_mod_dirs, BACKUP_MODS)
    worker.bundledFilePath = bundledFilePath

    worker.p = Pathing(createTemp_Config_ini)

    worker.start()

    assert os.path.isfile(f'{bundledFilePath}.zip')

    shutil.unpack_archive(f'{bundledFilePath}.zip', create_mod_dirs)

    assert os.listdir(bundledFilePath) == ['mods', 'assets', 'Maps']
    assert os.listdir(os.path.join(bundledFilePath, 'mods')) == ['make game easy mod']
    assert os.listdir(os.path.join(bundledFilePath, 'assets', 'mod_overrides')) == ['best mod ever']
    assert os.listdir(os.path.join(bundledFilePath, 'Maps')) == ['super fun mod']
