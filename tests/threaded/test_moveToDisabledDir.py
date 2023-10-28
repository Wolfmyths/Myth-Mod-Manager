import os

from src.threaded.moveToDisabledDir import MoveToDisabledDir
from src.getPath import Pathing
from src.save import OptionsManager, Save


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    dispath = os.path.join(create_mod_dirs, 'disabledMods')
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.setDispath(dispath)
    parser.writeData()

    thread = MoveToDisabledDir()
    thread.saveManager = Save(createTemp_Mod_ini)
    thread.optionsManager = parser

    thread.p = Pathing(createTemp_Config_ini)

    thread.moveToDisabledDir('make game easy mod')

    assert os.path.isdir(os.path.join(create_mod_dirs, 'disabledMods', 'make game easy mod'))
    assert not os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod'))
