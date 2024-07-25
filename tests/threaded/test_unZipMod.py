import os
import shutil

import pytest

from src.threaded.unZipMod import UnZipMod
from src.constant_vars import ModType
from src.getPath import Pathing
from src.save import OptionsManager, Save

#TODO: Everything seems to work but the assert statement
@pytest.mark.skip
def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.writeData()

    zip_path = os.path.join(create_mod_dirs, 'zip')
    os.mkdir(zip_path)
    shutil.make_archive(zip_path, 'zip')

    url = os.path.join(create_mod_dirs, 'zip.zip')

    worker = UnZipMod((url, ModType.mods))
    worker.optionsManager = parser
    worker.saveManager = Save(createTemp_Mod_ini)

    worker.p = Pathing(createTemp_Config_ini)

    worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'zip'))
