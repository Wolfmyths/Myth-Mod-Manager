import os
import logging
from typing import Self, Any

from configparser import ConfigParser

from src.constant_vars import MOD_CONFIG, OPTIONS_CONFIG, OPTIONS_SECTION, MOD_ENABLED, MOD_TYPE, ModType

class Config(ConfigParser):
    '''Base class for config managers'''

    file: str = None

    def __init__(self):
        super().__init__()

        logging.getLogger(__name__)

        # Ensuring that file exists
        if not os.path.exists(self.file):
            logging.warning('%s does not exist, creating...', self.file)
        
            # Create a new .ini
            with open(self.file, 'w') as f:
                pass
            
        self.read(self.file)
    
    def writeData(self) -> None:
        '''Writes data to the file this class is inherited by'''

        with open(self.file, 'w+') as f:

            self.write(f)

        logging.debug('%s has been saved', self.file)

class Save(Config):
    '''Manages the data of each mod'''

    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(Save, cls).__new__(cls)

        return cls.instance

    file = MOD_CONFIG

    def addMods(self, *mods: tuple[list[str] | str, ModType]) -> None:
        '''
        Saves new mods to the config file

        It takes both singular and lists of mods
        '''

        for arg in mods:
            
            if type(arg[0]) == list:

                for mod in arg[0]:

                    self.__newMod(mod, arg[1])

            else:

                self.__newMod(arg[0], arg[1])
        
        self.writeData()
    
    def isEnabled(self, mod: str) -> bool:
        '''Returns if the mod is enabled or not'''
        return self.getboolean(mod, MOD_ENABLED, fallback=False)
    
    def getType(self, mod: str) -> ModType | None:
        '''Returns the mod's type, if the mod doesn't exist then returns None'''

        modType = self.get(mod, MOD_TYPE, fallback=None)

        if modType is not None:
            return ModType(modType)
        else:
            return None
    
    def __newMod(self, mod: str, type: ModType) -> None:
            '''
            Adds a new mod to config.ini

            This function is mostly for `addMods()`
            
            **Does not save progress**
            '''

            if not self.has_section(mod):

                self.add_section(mod)
                self[mod][MOD_ENABLED] = 'True'
            
            self[mod][MOD_TYPE] = type.value

    def removeMods(self, *mods: str) -> None:
        '''Removes mods from MOD_CONFIG'''

        for mod in mods:

            self.remove_section(mod)
        
        self.writeData()

    def clearModData(self) -> None:
        '''Wipes the MOD_CONFIG's data'''

        logging.info('DELETING MODS FROM %s', MOD_CONFIG)

        self.clear()

        self.writeData()

class OptionsManager(Config):
    '''Manages Program's Settings'''

    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(OptionsManager, cls).__new__(cls)

        return cls.instance
    
    file = OPTIONS_CONFIG

    def setOption(self, value: str, option: str, section: str = OPTIONS_SECTION) -> None:
        '''
        Sets an option to the ini, if the section doesn't exist then it will be created
        
        Bool and int are also allowed for value but they need to be a string
        '''

        self.checkAddSection(section)
        
        self[section][option] = value

        self.writeData()

    def getOption(self, option: str, fallback= None, type: str | int | float | bool = str) -> Any:

        output = None

        if type == str:
            output = self.get(OPTIONS_SECTION, option, fallback=fallback)
        elif type == int:
            output = self.getint(OPTIONS_SECTION, option, fallback=fallback)
        elif type == float:
            output = self.getfloat(OPTIONS_SECTION, option, fallback=fallback)
        elif type == bool:
            output = self.getboolean(OPTIONS_SECTION, option, fallback=fallback)
        
        return output


    def checkAddSection(self, section: str) -> None:
        '''If a section doesn't exist then add it'''

        if not self.has_section(section):

            self.add_section(section)
