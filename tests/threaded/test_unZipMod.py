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

    thread = UnZipMod()
    thread.optionsManager = parser
    thread.saveManager = Save(createTemp_Mod_ini)

    thread.p = Pathing(createTemp_Config_ini)

    url = os.path.join(create_mod_dirs, 'zip.zip')

    thread.unZipMod((url, ModType.mods))

    assert os.path.exists(os.path.join(create_mod_dirs, 'mods', 'zip'))
