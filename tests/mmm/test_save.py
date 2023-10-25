import os

import pytest

from PySide6.QtCore import QSize

from src.constant_vars import ModKeys, OptionKeys, ModType
from src.save import Save, OptionsManager

EXPECTED_MODS = ('super fun mod', 'best mod ever', 'make game easy mod')

@pytest.mark.parametrize('modName', EXPECTED_MODS)
def test_testSave(createTemp_Mod_ini: str, modName: str) -> None:
    save = Save(createTemp_Mod_ini)

    assert save.has_section(modName)
    assert save.has_option(modName, ModKeys.type.value)
    assert save.has_option(modName, ModKeys.modworkshopid.value)

def test_saveMethods(createTemp_Mod_ini: str) -> None:

    save = Save(createTemp_Mod_ini)

    modName = 'funniest mod ever'

    save.addMods((modName, ModType.mods))
    assert save.has_section(modName)
    assert save.has_option(modName, ModKeys.type.value)
    assert save.getType(modName) == ModType.mods
    
    # Testing setters and getters (get/setType() is tested through the use of addMods())
    save.setEnabled(modName, False)
    assert save.has_option(modName, ModKeys.enabled.value)
    assert save.getEnabled(modName) == False

    save.setIgnored(modName, True)
    assert save.has_option(modName, ModKeys.ignored.value)
    assert save.getIgnored(modName) == True

    save.setModWorkshopAssetID(modName, '12345')
    assert save.has_option(modName, ModKeys.modworkshopid.value)
    assert save.getModworkshopAssetID(modName) == '12345'

    # Testing Sequence argument for addMods
    modsList = ['I hate my teammates mod', 'cats mod']

    save.addMods((modsList, ModType.mods_override))

    for mod in modsList:
        assert save.has_section(mod)
        assert save.has_option(mod, ModKeys.type.value)
        assert save.getType(mod) == ModType.mods_override

    save.removeMods(*modsList)
    
    for mod in modsList:
        assert save.has_section(mod) == False
    
    save.clearModData()

    assert len(save.sections()) == 0

def test_testOptions(createTemp_Config_ini: str, getDir: str) -> None:

    options = OptionsManager(createTemp_Config_ini)

    assert options.has_section(OptionKeys.section.value)
    assert options.has_option(OptionKeys.section.value, OptionKeys.game_path.value)
    assert options.getGamepath() == getDir
    assert options.has_option(OptionKeys.section.value, OptionKeys.dispath.value)
    assert options.getDispath() == os.path.join(getDir, 'disabledMods')

def test_OptionsMethods(createTemp_Config_ini: str) -> None:

    options = OptionsManager(createTemp_Config_ini)

    options.setDispath('somepath')
    assert options.getDispath() == 'somepath'

    options.setGamepath('somepath2')
    assert options.getGamepath() == 'somepath2'

    options.setTheme('somecolortheme')
    assert options.getTheme() == 'somecolortheme'

    options.setWindowSize(QSize(0, 0))
    assert options.getWindowSize() == QSize(0, 0)
