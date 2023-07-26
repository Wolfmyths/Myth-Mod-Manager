import os

from save import OptionsManager
from constant_vars import OPTIONS_SECTION, OPTIONS_GAMEPATH

def validGamePath() -> bool:

    optionsManager = OptionsManager()

    gamePath = optionsManager.get(OPTIONS_SECTION, OPTIONS_GAMEPATH, fallback=None)

    return os.path.exists(os.path.join(gamePath, 'payday2_win32_release.exe'))