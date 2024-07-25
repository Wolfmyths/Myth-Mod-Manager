from src.JSONParser import JSONParser

from src.constant_vars import PROFILES_JSON

class ProfileManager(JSONParser):
    file: dict[str:list[str]] = None
    def __init__(self, path: str = PROFILES_JSON) -> None:
        super().__init__(path)
    
    def __str__(self) -> str:

        if self.file is not None:
            output = str(self.file.items())
        else:
            output = 'None'
        
        return output
    
    def getMods(self, profile: str) -> list[str]:
        return self.file.get(profile)
    
    def getJSON(self) -> dict[str: list[str]]:
        return self.file

    def addProfile(self, *profiles: str) -> None:

        for profile in profiles:
            self.file[profile] = []

        self.saveJSON()

    def removeProfile(self, *profiles: str) -> None:

        for profile in profiles:
            self.file.pop(profile)

        self.saveJSON()
    
    def changeProfile(self, oldName: str, newName: str) -> None:

        oldNameDict: list[str] = self.getMods(oldName)

        self.file.pop(oldName)

        self.file[newName] = oldNameDict

        self.saveJSON()

    def addMod(self, profile: str, *mods: str) -> None:
        currentMods: list[str] = self.getMods(profile)

        newMods = [x for x in mods]
        

        updatedMods = list(set(currentMods + newMods))

        self.file[profile] = updatedMods

        self.saveJSON()

    def removeMod(self, profile: str, *mods: str) -> None:

        currentMods: list[str] = self.getMods(profile)

        for mod in mods:
            currentMods.remove(mod)
        
        self.file[profile] = currentMods

        self.saveJSON()