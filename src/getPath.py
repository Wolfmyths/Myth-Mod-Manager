import os

from src.save import OptionsManager
from src.constant_vars import ModType, OPTIONS_CONFIG

class Pathing():
    '''Getter functions that shorten the process of obtaining mod paths'''

    def __init__(self, optionFile: str = OPTIONS_CONFIG) -> None:
        self.option = optionFile
    
    def __getGamepath(self) -> str:
        return OptionsManager(self.option).getGamepath()
    
    def mod_overrides(self) -> str:
        '''Returns mod_overrides path'''
        return os.path.join(self.__getGamepath(), 'assets', 'mod_overrides')
    
    def mods(self) -> str:
        '''Returns mods directory path'''
        return os.path.join(self.__getGamepath(), 'mods')
    
    def maps(self) -> str:
        '''Returns maps directory path'''
        return os.path.join(self.__getGamepath(), 'Maps')
    
    def mod(self, type: ModType, modName: str) -> list[str] | str:
        '''
        Returns mod path given the type and name,
        does not check if the return value exists
        '''

        pathsDict = {ModType.mods : os.path.join(self.mods(), modName),
                    ModType.mods_override : os.path.join(self.mod_overrides(), modName),
                    ModType.maps : os.path.join(self.maps(), modName)}

        if type == ModType.all_types():
            return list(pathsDict.values())
        else:
            return pathsDict[type]
