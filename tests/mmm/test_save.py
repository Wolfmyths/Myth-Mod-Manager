import os

import pytest

from PySide6.QtCore import QSize

from src.constant_vars import ModKeys, OptionKeys, ModType
from src.save import Save, OptionsManager

EXPECTED_MODS = ('super fun mod', 'best mod ever', 'make game easy mod')

@pytest.mark.parametrize('modName', EXPECTED_MODS)
def test_testSave(createTemp_Mod_ini: str, modName: str) -> None:
    save = Save(createTemp_Mod_ini)

    assert save.hasMod(modName)
    assert save.hasModOption(modName, ModKeys.type.value)
    assert save.hasModOption(modName, ModKeys.modworkshopid.value)

def test_saveMethods(createTemp_Mod_ini: str) -> None:

    save = Save(createTemp_Mod_ini)

    modName = 'funniest mod ever'

    save.addMods((modName, ModType.mods))
    assert save.hasMod(modName)
    assert save.hasModOption(modName, ModKeys.type.value)
    assert save.getType(modName) == ModType.mods
    
    # Testing setters and getters (get/setType() is tested through the use of addMods())
    save.setEnabled(modName, False)
    assert save.hasModOption(modName, ModKeys.enabled.value)
    assert save.getEnabled(modName) == False

    save.setIgnored(modName, True)
    assert save.hasModOption(modName, ModKeys.ignored.value)
    assert save.getIgnored(modName) == True

    save.setModWorkshopAssetID(modName, '12345')
    assert save.hasModOption(modName, ModKeys.modworkshopid.value)
    assert save.getModworkshopAssetID(modName) == '12345'

    # Testing Sequence argument for addMods
    modsList = ['I hate my teammates mod', 'cats mod']

    save.addMods((modsList, ModType.mods_override))

    for mod in modsList:
        assert save.hasMod(mod)
        assert save.hasModOption(mod, ModKeys.type.value)
        assert save.getType(mod) == ModType.mods_override

    save.removeMods(*modsList)
    
    for mod in modsList:
        assert save.hasMod(mod) == False
    
    save.clearModData()

    assert len(save.mods()) == 0

def test_testOptions(createTemp_Config_ini: str, getDir: str) -> None:

    options = OptionsManager(createTemp_Config_ini)

    game_path = os.path.join(getDir, 'game_path')

    assert options.hasOption(OptionKeys.game_path.value)
    assert options.getGamepath() == game_path
    assert options.hasOption(OptionKeys.dispath.value)
    assert options.getDispath() == os.path.join(game_path, 'disabledMods')

def test_OptionsMethods(createTemp_Config_ini: str) -> None:

    options = OptionsManager(createTemp_Config_ini)

    options.setDispath('somepath')
    options.writeData()
    assert options.getDispath() == 'somepath'

    options.setGamepath('somepath2')
    options.writeData()
    assert options.getGamepath() == 'somepath2'

    options.setTheme('somecolortheme')
    options.writeData()
    assert options.getTheme() == 'somecolortheme'

    options.setWindowSize(QSize(0, 0))
    options.writeData()
    assert options.getWindowSize() == QSize(0, 0)
