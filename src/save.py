import os
import logging
from typing import TextIO, Sequence
from configparser import ConfigParser

from PySide6.QtCore import QSize

from src.JSONParser import JSONParser
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

        self.def_read()
    
    def getList(self, section: str, option: str, delimiter: str = ',') -> list:
        sequenceString = self.get(section, option, fallback=None)

        if isinstance(sequenceString, str) and sequenceString:
            sequence = sequenceString.split(delimiter)
            return sequence
        else:
            return []
 
    def setList(self, section: str, option: str, value: Sequence, delimiter: str = ',', sort: bool = False) -> None:
        if sort:
            value = sorted(value)

        list_ = delimiter.join(value)

        self.set(section, option, list_)
    
    def def_read(self) -> None:
        '''Short for default read, reads `self.file`'''
        return super().read(self.file)

    def writeData(self) -> None:
        with open(self.file, 'w') as f:
            f: TextIO
            self.write(f)

        logging.info('%s has been saved', self.file)

class Save(JSONParser):
    '''Manages the data of each mod'''

    def __init__(self, path=MOD_CONFIG):
        super().__init__(path=path)

    def mods(self) -> list[str]:
        return list(self.file.keys())
    
    def hasModOption(self, mod: str, option: str) -> bool:
        if self.hasMod(mod):
            return self.getMod(mod).get(option, None) is not None

        return False

    def hasMod(self, mod: str) -> bool:
        return self.getMod(mod) is not None

    def getMod(self, mod: str) -> dict | None:
        return self.file.get(mod, None)

    def addMods(self, *mods: tuple[list[str], ModType]) -> None:
        '''
        Saves new mods to the config file

        It takes both singular and lists of mods

        Param eg: `(List of mod names, ModType Enum)`
        '''

        for arg in mods:
            for mod in arg[0]:

                if not self.hasMod(mod):
                    logging.info('Adding new mod to %s: %s', MOD_CONFIG, mod)
                    self.file[mod] = {}

                self.setEnabled(mod)
                self.setType(mod, arg[1])

    def getEnabled(self, mod: str) -> bool:
        fallback = True
        if self.hasMod(mod):
            return self.getMod(mod).get(ModKeys.enabled.value, fallback)
        return fallback

    def setEnabled(self, mod: str, value: bool = True) -> None:
        if self.hasMod(mod):
            self.getMod(mod)[ModKeys.enabled.value] = value

    def getIgnored(self, mod: str) -> bool:
        fallback = False
        if self.hasMod(mod):
            return self.getMod(mod).get(ModKeys.ignored.value, fallback)
        else:
            return fallback

    def setIgnored(self, mod: str, value: bool = False) -> None:
        if self.hasMod(mod):
            self.getMod(mod)[ModKeys.ignored.value] = value
    
    def getType(self, mod: str) -> ModType | None:
        '''
        Converts the string into a `ModType` then returns it.
        Returns `None` if the mod doesn't have a type.
        '''

        if not self.hasMod(mod):
            logging.error('save.GetType: %s does not exist in the files', mod)
            return

        modType = self.getMod(mod).get(ModKeys.type.value)

        if modType is not None:
            return ModType(modType)
        else:
            return None
    
    def setType(self, mod: str, type: ModType) -> None:
        if self.hasMod(mod):
            self.getMod(mod)[ModKeys.type.value] = type
    
    def getModworkshopAssetID(self, mod: str) -> str:
        fallback = ''
        if self.hasMod(mod):
            return self.getMod(mod).get(ModKeys.modworkshopid, fallback)
        else:
            return fallback
    
    def setModWorkshopAssetID(self, mod: str, id: str = '') -> None:
        if self.hasMod(mod):
            self.getMod(mod)[ModKeys.modworkshopid.value] = id
    
    def getTags(self, mod: str) -> list[str]:
        fallback = []
        if self.hasMod(mod):
            tags = self.getMod(mod).get(ModKeys.tags.value, fallback)
            return tags if tags is not None else fallback
        else:
            return fallback
    
    def getAllTags(self) -> list[str]:
        allTags = set()
        for mod in self.mods():
            if not self.getTags(mod):
                continue
            for tag in self.getTags(mod):
                allTags.add(tag)

        return sorted(list(allTags))
    
    def setTags(self, tags: Sequence[str], *mods: str) -> None:
        if not tags:
            for mod in mods:
                if self.hasMod(mod):
                    self.getMod(mod)[ModKeys.tags] = None
            return

        for mod in mods:
            if not self.hasMod(mod):
                continue

            currentTags = self.getTags(mod)
            if currentTags is None:
                currentTags = []

            updatedTags = list(set(tags + currentTags))
            logging.info('Setting the tags of %s from %s to %s', mod, currentTags, updatedTags)

            self.getMod(mod)[ModKeys.tags.value] = updatedTags
    
    def removeTags(self, tags: Sequence[str], *mods: str) -> None:
        logging.info('Removing the tags %s from %')
        for mod in mods:
            modTags = self.getTags(mod)

            if not modTags:
                continue

            updatedTags = [x for x in modTags if x not in tags]
            logging.info('Removing the tags of %s from %s to %s', mod, modTags, updatedTags)

            self.getMod(mod)[ModKeys.tags] = updatedTags
    
    def clearTags(self) -> None:
        logging.info('CLEARING ALL TAGS')
        for mod in self.mods():
            self.getMod(mod)[ModKeys.tags] = None

    def removeMods(self, *mods: str) -> None:
        '''Removes mods from MOD_CONFIG'''

        logging.info('Removing mod(s): %s', ', '.join(mods))

        for mod in mods:
            self.file.pop(mod, None)

    def clearModData(self) -> None:
        '''Wipes the MOD_CONFIG's data'''

        logging.info('DELETING ALL MODS FROM %s', MOD_CONFIG)

        self.file = self.default

class OptionsManager(Config):
    '''Manages Program's Settings'''

    def __init__(self, file=OPTIONS_CONFIG):
        super().__init__(file=file)

        if not self.has_section(OptionKeys.section.value):
            self.add_section(OptionKeys.section.value)

    def hasOption(self, option: str) -> bool:
        return self.has_option(OptionKeys.section.value, option)

    def getMMMUpdateAlert(self) -> bool:
        self.def_read()
        return self.getboolean(OptionKeys.section.value, OptionKeys.mmm_update_alert.value, fallback=True)

    def setMMMUpdateAlert(self, alert: bool = True) -> None:
        self.set(OptionKeys.section.value, OptionKeys.mmm_update_alert.name, str(alert))

    def getTheme(self) -> str:
        self.def_read()
        return self.get(OptionKeys.section.value, OptionKeys.color_theme.name, fallback=LIGHT)

    def setTheme(self, theme: str = LIGHT) -> None:
        self.set(OptionKeys.section.value, OptionKeys.color_theme.value, theme)

    def getGamepath(self) -> str:
        self.def_read()
        return os.path.abspath(self.get(OptionKeys.section.value, OptionKeys.game_path, fallback=''))

    def setGamepath(self, path: str = '') -> None:
        self.set(OptionKeys.section.value, OptionKeys.game_path.name, os.path.abspath(path))

    def getDispath(self) -> str:
        self.def_read()
        return os.path.abspath(self.get(OptionKeys.section, OptionKeys.dispath, fallback=MODS_DISABLED_PATH_DEFAULT))

    def setDispath(self, path: str = MODS_DISABLED_PATH_DEFAULT) -> None:
        self.set(OptionKeys.section.value, OptionKeys.dispath.value, os.path.abspath(path))

    def getWindowSize(self) -> QSize:
        self.def_read()
        width = self.getint(OptionKeys.section.value, OptionKeys.windowsize_w.value, fallback=800)
        height = self.getint(OptionKeys.section.value, OptionKeys.windowsize_h.value, fallback=800)
        return QSize(width, height)

    def setWindowSize(self, size: QSize = QSize(800, 800)) -> None:
        self.set(OptionKeys.section.value, OptionKeys.windowsize_w.value, str(size.width()))
        self.set(OptionKeys.section.value, OptionKeys.windowsize_h.value, str(size.height()))
