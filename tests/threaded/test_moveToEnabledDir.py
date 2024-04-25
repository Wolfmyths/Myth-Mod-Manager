import os
import shutil

from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.getPath import Pathing
from src.save import OptionsManager


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    dispath = os.path.join(create_mod_dirs, 'disabledMods')
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.setDispath(dispath)
    parser.writeData()

    enabledDir = os.path.join(create_mod_dirs, 'mods', 'make game easy mod')
    disabledDir = os.path.join(create_mod_dirs, 'disabledMods', 'make game easy mod')

    shutil.move(enabledDir, disabledDir)

    worker = MoveToEnabledModDir('make game easy mod', optionsPath=createTemp_Config_ini, savePath=createTemp_Mod_ini)

    worker.p = Pathing(createTemp_Config_ini)

    worker.start()

    assert os.path.exists(enabledDir)
    assert not os.path.exists(disabledDir)
