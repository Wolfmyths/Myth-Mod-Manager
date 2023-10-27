import os
import logging
from typing import TextIO
from configparser import ConfigParser

from PySide6.QtCore import QSize

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG, ModType, LIGHT, MODS_DISABLED_PATH_DEFAULT, ModKeys, OptionKeys

class Config(ConfigParser):
    '''Base class for config managers'''

    def __init__(self, file: str = ''):
        super().__init__()
        logging.getLogger(__name__)

        self.file = file

        # Ensuring that file exists if file isn't a falsy value
        if not os.path.exists(self.file) and self.file:
            logging.warning('%s does not exist, creating...', self.file)

            # Create a new .ini
            with open(self.file, 'w+') as f:
                pass

        self.read(self.file)

    def writeData(self) -> None:
        with open(self.file, 'w') as f:
            f: TextIO
            self.write(f)

        logging.info('%s has been saved', self.file)

class Save(Config):
    '''Manages the data of each mod'''

    def __init__(self, file=MOD_CONFIG):
        super().__init__(file=file)

    def addMods(self, *mods: tuple[list[str] | str, ModType]) -> None:
        '''
        Saves new mods to the config file

        It takes both singular and lists of mods
        '''

        for arg in mods:

            if type(arg[0]) is list:

                for mod in arg[0]:

                    self.__newMod(mod, arg[1])

            else:

                self.__newMod(arg[0], arg[1])
    
    def __newMod(self, mod: str, type: ModType) -> None:
        '''
        Adds a new mod to config.ini

        This function is mostly for `addMods()`
        '''

        if not self.has_section(mod):
            self.add_section(mod)

        self.setEnabled(mod)

        self.setType(mod, type)
    
    def getEnabled(self, mod: str) -> bool:
        return self.getboolean(mod, ModKeys.enabled, fallback=False)
    
    def setEnabled(self, mod: str, value: bool = True) -> None:
        self.set(mod, ModKeys.enabled.value, str(value))

    def getIgnored(self, mod: str) -> bool:
        return self.getboolean(mod, ModKeys.ignored, fallback = False)

    def setIgnored(self, mod: str, value: bool = False) -> None:
        self.set(mod, ModKeys.ignored.value, str(value))
    
    def getType(self, mod: str) -> ModType | None:
        '''
        Converts the string into a `ModType` then returns it.
        Returns `None` if the mod doesn't have a type.
        '''

        modType = self.get(mod, ModKeys.type, fallback=None)

        if modType is not None:
            return ModType(modType)
        else:
            return None
    
    def setType(self, mod: str, type: ModType) -> None:
        self.set(mod, ModKeys.type.value, str(type))
    
    def getModworkshopAssetID(self, mod: str) -> str:
        return self.get(mod, ModKeys.modworkshopid, fallback='')
    
    def setModWorkshopAssetID(self, mod: str, id: str = '') -> None:
        self.set(mod, ModKeys.modworkshopid.value, id)

    def removeMods(self, *mods: str) -> None:
        '''Removes mods from MOD_CONFIG'''

        for mod in mods:

            self.remove_section(mod)

    def clearModData(self) -> None:
        '''Wipes the MOD_CONFIG's data'''

        logging.info('DELETING MODS FROM %s', MOD_CONFIG)

        self.clear()

class OptionsManager(Config):
    '''Manages Program's Settings'''

    def __init__(self, file: str = OPTIONS_CONFIG):
        super().__init__(file=file)

        if not self.has_section(OptionKeys.section.value):
            self.add_section(OptionKeys.section.value)

    def getTheme(self) -> str:
        return self.get(OptionKeys.section, OptionKeys.color_theme, fallback=LIGHT)
    
    def setTheme(self, theme: str = LIGHT) -> None:
        self.set(OptionKeys.section.value, OptionKeys.color_theme.value, theme)
    
    def getGamepath(self) -> str:
        return self.get(OptionKeys.section.value, OptionKeys.game_path, fallback='')
    
    def setGamepath(self, path: str = '') -> None:
        self.set(OptionKeys.section.value, OptionKeys.game_path.name, path)
    
    def getDispath(self) -> str:
        return self.get(OptionKeys.section, OptionKeys.dispath, fallback=MODS_DISABLED_PATH_DEFAULT)
    
    def setDispath(self, path: str = MODS_DISABLED_PATH_DEFAULT) -> None:
        self.set(OptionKeys.section.value, OptionKeys.dispath.value, path)
    
    def getWindowSize(self) -> QSize:
        width = self.getint(OptionKeys.section, OptionKeys.windowsize_w, fallback=800)
        height = self.getint(OptionKeys.section, OptionKeys.windowsize_h, fallback=800)
        return QSize(width, height)
    
    def setWindowSize(self, size: QSize = QSize(800, 800)) -> None:
        self.set(OptionKeys.section.value, OptionKeys.windowsize_w.value, str(size.width()))
        self.set(OptionKeys.section.value, OptionKeys.windowsize_h.value, str(size.height()))
