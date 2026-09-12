import os
import platform
from typing import LiteralString

from PySide6.QtCore import QSize

from src.constant_vars import OptionKeys
from src.helpers.options_manager import OptionsManager

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

    options.setProtonDirs(["path", "path2"])
    options.writeData()
    assert options.getProtonDirs() == ["path", "path2"]