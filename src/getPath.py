
import os

from save import OptionsManager
from constant_vars import OPTIONS_GAMEPATH, TYPE_MAPS, TYPE_MODS_OVERRIDE, TYPE_MODS, TYPE_ALL

class Pathing():
    '''Getter functions that shorten the process of obtaining mod paths'''

    def __init__(self) -> None:
        self.option = OptionsManager()
    
    def mod_overrides(self) -> str:
        '''Returns mod_overrides path'''
        gamePath = self.option.getOption(OPTIONS_GAMEPATH)
        return os.path.join(gamePath, 'assets', 'mod_overrides')
    
    def mods(self) -> str:
        '''Returns mods directory path'''
        gamePath = self.option.getOption(OPTIONS_GAMEPATH)
        return os.path.join(gamePath, 'mods')
    
    def maps(self) -> str:
        '''Returns maps directory path'''
        gamePath = self.option.getOption(OPTIONS_GAMEPATH)
        return os.path.join(gamePath, 'Maps')
    
    def mod(self, type: str, modName: str) -> list[str] | str | None:
        '''
        Returns mod path given the type and name,
        does not check if the return value exists
        
        If there's an invalid type, then return None
        '''

        pathsDict = {TYPE_MODS : os.path.join(self.mods(), modName),
                    TYPE_MODS_OVERRIDE : os.path.join(self.mod_overrides(), modName),
                    TYPE_MAPS : os.path.join(self.maps(), modName)}

        if type in list(pathsDict.keys()):
            
            return pathsDict[type]

        if type == TYPE_ALL:
            return list(pathsDict.values())