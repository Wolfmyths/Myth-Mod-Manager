import os
import logging

from src.JSONParser import JSONParser
from src.constant_vars import TOOLS_JSON

class ToolJSON(JSONParser):
    file: dict[str:list[str]] = None
    def __init__(self, path: str = TOOLS_JSON) -> None:
        logging.getLogger(__name__)
        super().__init__(path, default={'shortcuts' : []})
        self.path = path

    def __str__(self) -> str:

        if self.file is not None:
            output = str(self.file.get('shortcuts'))
        else:
            output = 'None'
        
        return output
    
    def getShortcuts(self) -> list[str]:
        return self.file.get('shortcuts')
    
    def newTool(self, *urls: str) -> list[str]:
        '''
        Adds new urls to the shortcuts list, returns a list of duplicates
        '''

        dupes: list[str] = []

        shortcuts = self.getShortcuts()

        for url in urls:
            if url not in shortcuts:
                shortcuts.append(os.path.abspath(url))
            else:
                dupes.append(url)
        
        self.file['shortcuts'] = shortcuts

        if dupes:
            logging.info('Duplicate URL shortcuts tried to be added: %s', ', '.join(dupes))

        return dupes
    
    def removeTool(self, *urls: str) -> None:
        shortcuts = self.getShortcuts()
        for url in urls:
            if url in shortcuts:
                logging.info('External tool at %s has been deleted', url)
                shortcuts.remove(url)
        
        self.file['shortcuts'] = shortcuts
    
    def changeTool(self, old: str, new: str) -> None:
        shortcuts = self.getShortcuts()
        if old in shortcuts:
            logging.info('External tool url has changed from %s to %s', old, new)
            index = shortcuts.index(os.path.abspath(old))
            shortcuts[index] = os.path.abspath(new)
        
        self.file['shortcuts'] = shortcuts
