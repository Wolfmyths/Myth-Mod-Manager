
import os
import logging
from typing import Self

from configparser import ConfigParser

from constant_vars import MOD_CONFIG, OPTIONS_CONFIG, OPTIONS_SECTION, MOD_ENABLED, MOD_TYPE

class Save(ConfigParser):
    def __init__(self) -> None:
        super().__init__()

        logging.getLogger(__name__)

        # Ensuring that MOD_CONFIG exists
        if not os.path.exists(MOD_CONFIG):
            logging.warning('%s does not exist, creating...', MOD_CONFIG)
            
            # Create a new .ini
            with open(MOD_CONFIG, 'w') as f:
                pass
            
        self.read(MOD_CONFIG)

    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(Save, cls).__new__(cls)

        return cls.instance

    def addMods(self, *mods: tuple[list[str] | str, str]) -> None:
        '''
        Saves new mods to the config file

        It takes both singular and lists of mods

        The 1st index of the tuple is the type
        '''

        for arg in mods:
            
            if type(arg[0]) == list:

                for mod in arg[0]:

                    self.newMod(mod, arg[1])

            else:

                self.newMod(arg[0], arg[1])
    
    def isEnabled(self, mod: str) -> bool:
        '''Returns if the mod is enabled or not'''
        return self.getboolean(mod, MOD_ENABLED, fallback=False)
    
    def getType(self, mod: str) -> str | None:
        '''Returns the mod's type, if the mod doesn't exist then returns None'''
        return self.get(mod, MOD_TYPE, fallback=None)
    
    def newMod(self, mod: str, type: str) -> None:
            '''
            Adds a new mod to config.ini
            
            This function is in-scope with addMods() to make an attempt at
            making an overloaded function
            '''

            if not self.has_section(mod):

                self.add_section(mod)
                self[mod][MOD_ENABLED] = 'True'
            
            self[mod][MOD_TYPE] = type

            self.writeData()

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

    def writeData(self) -> None:

        with open(MOD_CONFIG, 'w') as f:

            self.write(f)
        
        logging.debug('%s has been saved', MOD_CONFIG)

class OptionsManager(ConfigParser):
    def __init__(self) -> None:
        super().__init__()

        # Ensuring that OPTIONS_CONFIG exists
        if not os.path.exists(OPTIONS_CONFIG):
            logging.warning('%s does not exist, creating...', OPTIONS_CONFIG)

            # Create a new .ini
            with open(OPTIONS_CONFIG, 'w') as f:
                pass
        
        self.read(OPTIONS_CONFIG)

        if not self.has_section(OPTIONS_SECTION):
            self.add_section(OPTIONS_SECTION)
            self.writeData()
    
    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(OptionsManager, cls).__new__(cls)

        return cls.instance
    
    def setOption(self, value: str, option: str, section: str = OPTIONS_SECTION) -> None:
        '''
        Sets an option to the ini, if the section doesn't exist then it will be created
        
        Bool and int are also allowed for value but they need to be a string
        '''

        self.checkAddSection(section)
        
        self[section][option] = value

        self.writeData()

    def getOption(self, option: str, fallback= None) -> str | None:
        return self.get(OPTIONS_SECTION, option, fallback=fallback)

    def checkAddSection(self, section: str) -> None:
        '''If a section doesn't exist then add it'''

        if not self.has_section(section):

            self.add_section(section)
    
    def writeData(self) -> None:

        with open(OPTIONS_CONFIG, 'w+') as f:

            self.write(f)

        logging.debug('%s has been saved', OPTIONS_CONFIG)