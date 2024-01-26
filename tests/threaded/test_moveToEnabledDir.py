import os
import shutil

from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.getPath import Pathing
from src.save import OptionsManager, Save


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    dispath = os.path.join(create_mod_dirs, 'disabledMods')
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.setDispath(dispath)
    parser.writeData()

    enabledDir = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')
    disabledDir = os.path.join(create_mod_dirs, 'disabledMods', 'make game easy mod')

    shutil.move(enabledDir, disabledDir)

    worker = MoveToEnabledModDir('make game easy mod')
    worker.saveManager = Save(createTemp_Mod_ini)
    worker.optionsManager = parser

    worker.p = Pathing(createTemp_Config_ini)

    worker.start()

    assert os.path.isdir(enabledDir)
    assert not os.path.isdir(disabledDir)
