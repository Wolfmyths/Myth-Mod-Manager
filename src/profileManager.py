from typing import Self
import json

from src.constant_vars import PROFILES_JSON

class ProfileManager():
    file: dict[str:list[str]] = None

    def __init__(self) -> None:
        try:
            self.__loadJSON()
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open(PROFILES_JSON, 'w') as f:
                f.write(json.dumps({}))
            
            self.__loadJSON()
    
    def __new__(cls) -> Self:

        if not hasattr(cls, 'instance'):

            cls.instance = super(ProfileManager, cls).__new__(cls)

        return cls.instance

    def __str__(self) -> str:

        if self.file is not None:
            output = str(self.file.items())
        else:
            output = 'None'
        
        return output

    def __makeElementsUnique(self, l: list) -> list:
        '''Used to make sure there aren't any duplicate mod entries in said iterable'''
        list_set = set(l)
        return list(list_set)

    def __loadJSON(self):
        with open(PROFILES_JSON, 'r') as f:
            self.file = json.loads(f.read())

    def __saveJSON(self):
        with open(PROFILES_JSON, 'w') as f:
            f.seek(0)
            f.write(json.dumps(self.file, indent=2))
            f.truncate()
    
    def getMods(self, profile: str) -> list[str]:
        return self.file.get(profile)
    
    def getJSON(self) -> dict[str: list[str]]:
        return self.file

    def addProfile(self, *profiles: str):

        for profile in profiles:
            self.file[profile] = []

        self.__saveJSON()

    def removeProfile(self, *profiles: str):

        for profile in profiles:
            self.file.pop(profile)

        self.__saveJSON()
    
    def changeProfile(self, oldName: str, newName: str):

        oldNameDict: list[str] = self.file.get(oldName)

        self.file.pop(oldName)

        self.file[newName] = oldNameDict

        self.__saveJSON()

    def addMod(self, profile: str, *mods: str):

        newMods = [x for x in mods]
        currentMods: list[str] = self.file.get(profile)

        updatedMods = self.__makeElementsUnique(currentMods + newMods)

        self.file[profile] = updatedMods

        self.__saveJSON()

    def removeMod(self, profile: str, *mods: str):

        currentMods: list[str] = self.file.get(profile)

        for mod in mods:
            currentMods.remove(mod)
        
        self.file[profile] = currentMods

        self.__saveJSON()