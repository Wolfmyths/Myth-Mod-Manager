import os
import logging
from typing import Sequence, TextIO
from configparser import ConfigParser

from PySide6.QtCore import QSize

from src.constant_vars import OptionKeys, OPTIONS_CONFIG, LIGHT, MODS_DISABLED_PATH_DEFAULT

class OptionsManager():
    '''Manages Program's Settings'''

    config = ConfigParser()
    file: str = ''

    def __init__(self, file=OPTIONS_CONFIG) -> None:

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
    def getList(section: str, option: str, delimiter: str = ',') -> list:
        sequenceString = OptionsManager.config.get(section, option, fallback=None)

        if isinstance(sequenceString, str) and sequenceString:
            sequence = sequenceString.split(delimiter)
            return sequence
        else:
            return []
    
    @staticmethod
    def setList(section: str, option: str, value: Sequence, delimiter: str = ',', sort: bool = False) -> None:
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
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.launch_parameters.value, fallback='')

    @staticmethod
    def setLaunchParameters(params: str = '') -> str:
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
    def getGamepath() -> str:
        return os.path.abspath(OptionsManager.config.get(OptionKeys.section.value, OptionKeys.game_path, fallback=''))

    @staticmethod
    def setGamepath(path: str = '') -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.game_path.name, os.path.abspath(path))

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
    def setWindowSize(size: QSize = QSize(800, 800)) -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.windowsize_w.value, str(size.width()))
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.windowsize_h.value, str(size.height()))
    
    @staticmethod
    def getLang() -> str:
        return OptionsManager.config.get(OptionKeys.section.value, OptionKeys.lang.value, fallback='en_US')

    @staticmethod
    def setLang(lang: str = 'en_US') -> None:
        OptionsManager.config.set(OptionKeys.section.value, OptionKeys.lang.value, lang)
