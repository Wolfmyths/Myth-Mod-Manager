import os

from src.helpers.options_manager import OptionsManager
from src.constant_vars import ModType

class Pathing():
    '''Getter functions that shorten the process of obtaining mod paths'''

    @staticmethod
    def mod_overrides() -> str:
        '''Returns mod_overrides path'''
        return os.path.join(OptionsManager.getGamepath(), 'assets', 'mod_overrides')

    @staticmethod
    def mods() -> str:
        '''Returns mods directory path'''
        return os.path.join(OptionsManager.getGamepath(), 'mods')

    @staticmethod
    def maps() -> str:
        '''Returns maps directory path'''
        return os.path.join(OptionsManager.getGamepath(), 'Maps')

    @staticmethod
    def mod(type: ModType, modName: str) -> list[str] | str:
        '''
        Returns mod path given the type and name,
        does not check if the return value exists
        '''

        pathsDict: dict[ModType, str] = {
            ModType.mods : os.path.join(Pathing.mods(), modName),
            ModType.mods_override : os.path.join(Pathing.mod_overrides(), modName),
            ModType.maps : os.path.join(Pathing.maps(), modName)
        }

        if type == ModType.all_types():
            return list(pathsDict.values())
        else:
            return pathsDict[type]
