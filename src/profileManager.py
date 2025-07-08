from src.JSONParser import JSONParser

from src.constant_vars import PROFILES_JSON

class ProfileManager():
    _file: dict[str:list[str]] = None
    _path: str = ''

    def __init__(self, path: str = PROFILES_JSON) -> None:
        ProfileManager._file = JSONParser.loadJSON(path)
        ProfileManager._path = path
    
    def __str__() -> str:

        if ProfileManager._file is not None:
            output = str(ProfileManager._file.items())
        else:
            output = 'None'
        
        return output
    
    @staticmethod
    def _save() -> None:
        JSONParser.saveJSON(PROFILES_JSON, ProfileManager._file)

    @staticmethod
    def get_profile_names() -> list[str]:
        return list(ProfileManager._file.keys())

    @staticmethod
    def getMods(profile: str) -> list[str]:
        return ProfileManager._file.get(profile)
    
    @staticmethod
    def getJSON() -> dict[str: list[str]]:
        return ProfileManager._file

    @staticmethod
    def addProfile(*profiles: str) -> None:

        for profile in profiles:
            ProfileManager._file[profile] = []

        ProfileManager._save()

    @staticmethod
    def removeProfile(*profiles: str) -> None:

        for profile in profiles:
            ProfileManager._file.pop(profile)

        ProfileManager._save()
    
    @staticmethod
    def changeProfile(oldName: str, newName: str) -> None:

        oldNameDict: list[str] = ProfileManager.getMods(oldName)

        ProfileManager._file.pop(oldName)

        ProfileManager._file[newName] = oldNameDict

        ProfileManager._save()

    @staticmethod
    def addMod(profile: str, *mods: str) -> None:
        currentMods: list[str] = ProfileManager.getMods(profile)

        newMods: list[str] = [x for x in mods]
        

        updatedMods: list[str] = list(set(currentMods + newMods))

        ProfileManager._file[profile] = updatedMods

        ProfileManager._save()

    @staticmethod
    def removeMod(profile: str, *mods: str) -> None:

        currentMods: list[str] = ProfileManager.getMods(profile)

        for mod in mods:
            currentMods.remove(mod)
        
        ProfileManager._file[profile] = currentMods

        ProfileManager._save()