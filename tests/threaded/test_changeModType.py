import os

from src.threaded.changeModType import ChangeModType
from src.constant_vars import ModType
from src.getPath import Pathing
from src.save import OptionsManager, Save


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.writeData()

    url = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')

    worker = ChangeModType((url, ModType.mods_override))
    worker.saveManager = Save(createTemp_Mod_ini)
    worker.p = Pathing(createTemp_Config_ini)

    worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) == False
    assert os.path.isdir(os.path.join(create_mod_dirs, 'assets', 'mod_overrides', 'make game easy mod'))
