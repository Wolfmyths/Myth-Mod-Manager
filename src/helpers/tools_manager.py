import os
import logging

from typing_extensions import override

from src.helpers.json_parser import JSONParser
from src.constant_vars import TOOLS_JSON

class ToolJSON():
    _file: dict[str, list[str]] = {}
    _path: str = ''

    def __init__(self, path: str = TOOLS_JSON) -> None:
        logging.getLogger(__name__)

        ToolJSON._file = JSONParser.loadJSON(path, {'shortcuts' : []})
        ToolJSON._path = path

    @override
    def __str__(self) -> str:

        if not ToolJSON._file:
            output = str(ToolJSON._file.get('shortcuts'))
        else:
            output = 'None'
        
        return output
    
    @staticmethod
    def save() -> None:
        JSONParser.saveJSON(ToolJSON._path, ToolJSON._file)

    @staticmethod
    def getShortcuts() -> list[str]:
        return ToolJSON._file.get('shortcuts', [])
    
    @staticmethod
    def newTool(*urls: str) -> list[str]:
        '''
        Adds new urls to the shortcuts list, returns a list of duplicates
        '''

        dupes: list[str] = []

        shortcuts: list[str] = ToolJSON.getShortcuts()

        for url in urls:
            if url not in shortcuts:
                shortcuts.append(os.path.abspath(url))
            else:
                dupes.append(url)
        
        ToolJSON._file['shortcuts'] = shortcuts

        if dupes:
            logging.info('Duplicate URL shortcuts tried to be added: %s', ', '.join(dupes))

        return dupes
    
    @staticmethod
    def removeTool(*urls: str) -> None:
        shortcuts: list[str] = ToolJSON.getShortcuts()
        for url in urls:
            if url in shortcuts:
                logging.info('External tool at %s has been deleted', url)
                shortcuts.remove(url)
        
        ToolJSON._file['shortcuts'] = shortcuts
    
    @staticmethod
    def changeTool(old: str, new: str) -> None:
        shortcuts: list[str] = ToolJSON.getShortcuts()
        if old in shortcuts:
            logging.info('External tool url has changed from %s to %s', old, new)
            index: int = shortcuts.index(os.path.abspath(old))
            shortcuts[index] = os.path.abspath(new)
        
        ToolJSON._file['shortcuts'] = shortcuts
