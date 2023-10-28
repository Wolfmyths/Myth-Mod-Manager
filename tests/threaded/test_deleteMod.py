import os
import shutil

from src.threaded.deleteMod import DeleteMod
from src.getPath import Pathing
from src.save import OptionsManager, Save


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.writeData()

    thread = DeleteMod()
    thread.optionsManager = parser
    thread.saveManager = Save(createTemp_Mod_ini)

    thread.p = Pathing(createTemp_Config_ini)

    thread.deleteMod('make game easy mod')

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) == False
