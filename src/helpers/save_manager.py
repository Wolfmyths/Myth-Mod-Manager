import logging
from typing import Sequence

from src.helpers.json_parser import JSONParser
from src.constant_vars import MOD_CONFIG, ModType, ModKeys

class Save():
    '''Manages the data of each mod'''

    _file: dict = {}
    _path: str = ''

    def __init__(self, file=MOD_CONFIG) -> None:
        Save._path = file
        Save._file = JSONParser.loadJSON(file)

    @staticmethod
    def saveJSON() -> None:
        JSONParser.saveJSON(Save._path, Save._file)

    @staticmethod
    def mods() -> list[str]:
        return list(Save._file.keys())
    
    @staticmethod
    def hasModOption(mod: str, option: str) -> bool:
        if Save.hasMod(mod):
            return option in Save.getMod(mod)

        return False

    @staticmethod
    def hasMod(mod: str) -> bool:
        return Save.getMod(mod) is not None

    @staticmethod
    def getMod(mod: str) -> dict:
        return Save._file.get(mod, None)

    @staticmethod
    def addMods(*mods: tuple[list[str], ModType]) -> None:
        '''
        Saves new mods to the config file

        It takes both singular and lists of mods

        Param eg: `(List of mod names, ModType Enum)`
        '''

        for arg in mods:
            for mod in arg[0]:

                if not Save.hasMod(mod):
                    logging.info('Adding new mod to %s: %s', MOD_CONFIG, mod)
                    Save._file[mod] = {}

                Save.setEnabled(mod)
                Save.setType(mod, arg[1])

    @staticmethod
    def getEnabled(mod: str) -> bool:
        fallback = True
        if Save.hasMod(mod):
            return Save.getMod(mod).get(ModKeys.enabled.value, fallback)
        return fallback

    @staticmethod
    def setEnabled(mod: str, value: bool = True) -> None:
        if Save.hasMod(mod):
            Save.getMod(mod)[ModKeys.enabled.value] = value

    @staticmethod
    def getIgnored(mod: str) -> bool:
        fallback = False
        if Save.hasMod(mod):
            return Save.getMod(mod).get(ModKeys.ignored.value, fallback)
        else:
            return fallback

    @staticmethod
    def setIgnored(mod: str, value: bool = False) -> None:
        if Save.hasMod(mod):
            Save.getMod(mod)[ModKeys.ignored.value] = value
    
    @staticmethod
    def getType(mod: str) -> ModType | None:
        '''
        Converts the string into a `ModType` then returns it.
        Returns `None` if the mod doesn't have a type.
        '''

        if not Save.hasMod(mod):
            logging.error('save.GetType: %s does not exist in the files', mod)
            return

        modType = Save.getMod(mod).get(ModKeys.type.value)

        if modType:
            return ModType(modType)
        else:
            return None
    
    @staticmethod
    def setType(mod: str, type: ModType) -> None:
        if Save.hasMod(mod):
            Save.getMod(mod)[ModKeys.type.value] = type
    
    @staticmethod
    def getModworkshopAssetID(mod: str) -> str:
        fallback = ''
        if Save.hasMod(mod):
            return Save.getMod(mod).get(ModKeys.modworkshopid, fallback)
        else:
            return fallback
    
    @staticmethod
    def setModWorkshopAssetID(mod: str, id: str = '') -> None:
        if Save.hasMod(mod):
            Save.getMod(mod)[ModKeys.modworkshopid.value] = id
    
    @staticmethod
    def getTags(mod: str) -> list[str]:
        fallback = []
        if Save.hasMod(mod):
            tags = Save.getMod(mod).get(ModKeys.tags.value, fallback)
            return tags if tags is not None else fallback
        else:
            return fallback
    
    @staticmethod
    def getAllTags() -> list[str]:
        allTags = set()
        for mod in Save.mods():
            if not Save.getTags(mod):
                continue
            for tag in Save.getTags(mod):
                allTags.add(tag)

        return sorted(list(allTags))
    
    @staticmethod
    def setTags(tags: Sequence[str], *mods: str) -> None:
        if not tags:
            for mod in mods:
                if Save.hasMod(mod):
                    Save.getMod(mod)[ModKeys.tags] = None
            return

        for mod in mods:
            if not Save.hasMod(mod):
                continue

            currentTags = Save.getTags(mod)
            if currentTags is None:
                currentTags = []

            updatedTags = list(set(tags + currentTags))
            logging.info('Setting the tags of %s from %s to %s', mod, currentTags, updatedTags)

            Save.getMod(mod)[ModKeys.tags.value] = updatedTags
    
    @staticmethod
    def removeTags(tags: Sequence[str], *mods: str) -> None:
        logging.info('Removing the tags %s from %')
        for mod in mods:
            modTags = Save.getTags(mod)

            if not modTags:
                continue

            updatedTags = [x for x in modTags if x not in tags]
            logging.info('Removing the tags of %s from %s to %s', mod, modTags, updatedTags)

            Save.getMod(mod)[ModKeys.tags] = updatedTags
    
    @staticmethod
    def clearTags() -> None:
        logging.info('CLEARING ALL TAGS')
        for mod in Save.mods():
            Save.getMod(mod)[ModKeys.tags] = None

    @staticmethod
    def removeMods(*mods: str) -> None:
        '''Removes mods from MOD_CONFIG'''

        logging.info('Removing mod(s): %s', ', '.join(mods))

        for mod in mods:
            Save._file.pop(mod, None)

    @staticmethod
    def clearModData() -> None:
        '''Wipes the MOD_CONFIG's data'''

        logging.info('DELETING ALL MODS FROM %s', MOD_CONFIG)

        Save._file = {}
