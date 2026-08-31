import os
import platform
import logging
from typing import Any, LiteralString, TextIO
from collections.abc import Sequence
from configparser import ConfigParser

from PySide6.QtCore import QSize

from src.constant_vars import OptionKeys, OPTIONS_CONFIG, LIGHT, MODS_DISABLED_PATH_DEFAULT, STEAM

class OptionsManager():
    '''Manages Program's Settings'''

    config = ConfigParser()
    file: str = ''

    DEFAULT_WINDOW_SIZE = QSize(800, 800)

    def __init__(self, file: str = OPTIONS_CONFIG) -> None:

        OptionsManager.file = file

        # Ensuring that file exists if file isn't a falsy value
        if not os.path.exists(OptionsManager.file) and OptionsManager.file:
            logging.warning('%s does not exist, creating...', OptionsManager.file)

            # Create a new .ini
            with open(OptionsManager.file, 'w+') as _f:
                pass

        OptionsManager.read()

        if not OptionsManager.config.has_section(OptionKeys.section.value):
            OptionsManager.config.add_section(OptionKeys.section.value)
    
    @staticmethod
    def getList(section: str, option: str, delimiter: str = ',') -> list[Any]:
        sequenceString = OptionsManager.config.get(section, option, fallback=None)

        if isinstance(sequenceString, str) and sequenceString:
            sequence = sequenceString.split(delimiter)
            return sequence
        else:
            return []
    
    @staticmethod
    def setList(section: str, option: str, value: Sequence[Any], delimiter: str = ',', sort: bool = False) -> None:
        if sort:
            value = sorted(value)

        list_: str = delimiter.join(value)

        OptionsManager.config.set(section, option, list_)
    
    @staticmethod
    def read() -> list[str]:
        '''Reads `OptionsManager.file`'''
        return OptionsManager.config.read(OptionsManager.file)

    @staticmethod
    def writeData() -> None:
        with open(OptionsManager.file, 'w') as f:
            f: TextIO
            OptionsManager.config.write(f)

        logging.info('%s has been saved', OptionsManager.file)
    
    @staticmethod
    def hasOption(option: str) -> bool:
        return OptionsManager.config.has_option(OptionKeys.section.value, option)

    @staticmethod
    def getLaunchParameters() -> str:
        """
        Launch parameters for PAYDAY 2. If you want it casted into `list[str]` see `OptionsManager.getLaunchParametersList()`
        """
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.launch_parameters.value, fallback='')
    
    # Launch parameters but is converted into a list
    @staticmethod
    def getLaunchParametersList() -> list[str]:
        args = OptionsManager.getLaunchParameters().split("-")

        for i in range(len(args)):
            args[i] = f"-{args[i]}"
        
        return args

    @staticmethod
    def setLaunchParameters(params: str = '') -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.launch_parameters.value, params)

    @staticmethod
    def getMMMUpdateAlert() -> bool:
        return OptionsManager.config.getboolean(OptionKeys.section.value, OptionKeys.mmm_update_alert.value, fallback=True)

    @staticmethod
    def setMMMUpdateAlert(alert: bool = True) -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.mmm_update_alert.name, str(alert))

    @staticmethod
    def getTheme() -> str:
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.color_theme.name, fallback=LIGHT)

    @staticmethod
    def setTheme(theme: str = LIGHT) -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.color_theme.value, theme)

    @staticmethod
    def getGameExecuteable() -> str:
        fallback: str
        if platform.system().startswith("Win"):
            fallback = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\PAYDAY 2\\PAYDAY2.exe"
        else:
            fallback = f"{STEAM}/steamapps/common/PAYDAY 2/PAYDAY2.exe"
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.game_path, fallback=fallback)

    @staticmethod
    def setGameExecuteable(path: str = '') -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.game_path.name, path)

    @staticmethod
    def getGamepath() -> str:
        '''Returns the path of the game executable's directory'''
        return os.path.dirname(OptionsManager.getGameExecuteable())

    @staticmethod
    def getDispath() -> str:
        return os.path.abspath(OptionsManager.config.get(OptionKeys.section, OptionKeys.dispath, fallback=MODS_DISABLED_PATH_DEFAULT))

    @staticmethod
    def setDispath(path: str = MODS_DISABLED_PATH_DEFAULT) -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.dispath.value, os.path.abspath(path))

    @staticmethod
    def getWindowSize() -> QSize:
        width = OptionsManager.config.getint(OptionKeys.section.value, OptionKeys.windowsize_w.value, fallback=800)
        height = OptionsManager.config.getint(OptionKeys.section.value, OptionKeys.windowsize_h.value, fallback=800)
        return QSize(width, height)

    @staticmethod
    def setWindowSize(size: QSize = DEFAULT_WINDOW_SIZE) -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.windowsize_w.value, str(size.width()))
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.windowsize_h.value, str(size.height()))
    
    @staticmethod
    def getLang() -> str:
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.lang.value, fallback='en_US')

    @staticmethod
    def setLang(lang: str = 'en_US') -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.lang.value, lang)
    
    @staticmethod
    def getProtonVersion() -> str:
        return OptionsManager.config.get(OptionKeys.section, OptionKeys.proton_version, fallback="")

    @staticmethod
    def setProtonVersion(version: str) -> None:
        OptionsManager.config.set(OptionKeys.section, OptionKeys.proton_version, version)
