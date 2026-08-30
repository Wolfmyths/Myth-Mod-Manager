import os
import platform
from typing import LiteralString

import pytest

from PySide6.QtCore import QSize

from src.constant_vars import ModKeys, OptionKeys, ModType
from src.helpers.options_manager import OptionsManager
from src.helpers.save_manager import Save

EXPECTED_MODS = ('super fun mod', 'best mod ever', 'make game easy mod')

@pytest.mark.parametrize('modName', EXPECTED_MODS)
def test_testSave(createTemp_Mod_ini: str, modName: str) -> None:
    save = Save(createTemp_Mod_ini)

    assert save.hasMod(modName)
    assert save.hasModOption(modName, ModKeys.type.value)
    assert save.hasModOption(modName, ModKeys.modworkshopid.value) is not False

def test_saveMethods(createTemp_Mod_ini: str) -> None:

    save = Save(createTemp_Mod_ini)

    modName = 'super fun mod'
    
    # Testing setters and getters (get/setType() is tested through the use of addMods())
    save.setEnabled(modName, False)
    assert save.hasModOption(modName, ModKeys.enabled.value)
    assert not save.getEnabled(modName)

    save.setIgnored(modName, True)
    assert save.hasModOption(modName, ModKeys.ignored.value)
    assert save.getIgnored(modName)

    save.setModWorkshopAssetID(modName, '12345')
    assert save.hasModOption(modName, ModKeys.modworkshopid.value)
    assert save.getModworkshopAssetID(modName) == '12345'

    # Testing Sequence argument for addMods
    modsList: list[str] = ['I hate my teammates mod', 'cats mod']

    save.addMods((modsList, ModType.mods_override))

    for mod in modsList:
        assert save.hasMod(mod)
        assert save.hasModOption(mod, ModKeys.type.value)
        assert save.getType(mod) == ModType.mods_override

    save.removeMods(*modsList)
    
    for mod in modsList:
        assert not save.hasMod(mod)
    
    save.clearModData()

    assert len(save.mods()) == 0

def test_testOptions(createTemp_Config_ini: str, create_mod_dirs: str) -> None:

    options = OptionsManager(createTemp_Config_ini)

    assert options.hasOption(OptionKeys.game_path.value)
    assert options.getGamepath() == create_mod_dirs
    assert options.hasOption(OptionKeys.dispath.value)
    assert options.getDispath() == os.path.join(create_mod_dirs, 'disabledMods')

def test_OptionsMethods(createTemp_Config_ini: str) -> None:

    options = OptionsManager(createTemp_Config_ini)
    expected_fallback_path: LiteralString

    if platform.system().startswith("Win"):
        expected_fallback_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\PAYDAY 2\\PAYDAY2.exe"
    else:
        expected_fallback_path ="~/.local/share/Steam/SteamApps/common/PAYDAY 2/PAYDAY2.exe"

    options.setDispath('somepath')
    options.writeData()
    assert os.path.basename(options.getDispath()) == 'somepath'

    # Check fallback value
    options.config.remove_option(OptionKeys.section, OptionKeys.game_path)
    assert options.getGameExecuteable() == expected_fallback_path

    options.setGameExecuteable(os.path.abspath(os.path.join('somepath2', 'game.exe')))
    options.writeData()
    assert os.path.basename(options.getGamepath()) == "somepath2"
    assert os.path.basename(options.getGameExecuteable()) == "game.exe"

    options.setTheme('somecolortheme')
    options.writeData()
    assert options.getTheme() == 'somecolortheme'

    options.setWindowSize(QSize(0, 0))
    options.writeData()
    assert options.getWindowSize() == QSize(0, 0)

    options.setMMMUpdateAlert(False)
    options.writeData()
    assert not options.getMMMUpdateAlert()

    options.setLang('language')
    options.writeData()
    assert options.getLang() == 'language'

    options.setGameExecuteable('exe')
    options.writeData()
    assert options.getGameExecuteable() == "exe"

    options.setProtonVersion("2.0")
    options.writeData()
    assert options.getProtonVersion() == "2.0"
