import json
import os
import logging

from src.constant_vars import TOOLS_JSON

class ToolJSON():
    file: dict[str:list[str]] = None
    def __init__(self, path: str = TOOLS_JSON) -> None:
        logging.getLogger(__name__)
        self.path = path
        try:
            self.__loadJSON()
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open(self.path, 'w') as f:
                f.write(json.dumps({'shortcuts' : []}))
            
            self.__loadJSON()

    def __str__(self) -> str:

        if self.file is not None:
            output = str(self.file.get('shortcuts'))
        else:
            output = 'None'
        
        return output

    def __loadJSON(self):
        with open(self.path, 'r') as f:
            self.file = json.loads(f.read())

    def __saveJSON(self):
        logging.debug('External tools have been saved')
        with open(TOOLS_JSON, 'w') as f:
            f.seek(0)
            f.write(json.dumps(self.file, indent=2))
            f.truncate()
    
    def getShortcuts(self) -> list[str]:
        return self.file['shortcuts']
    
    def newTool(self, *urls: str) -> list[str]:
        '''
        Adds new urls to the shortcuts list, returns a list of duplicates
        '''

        dupes: list[str] = []

        for url in urls:
            if url not in self.file['shortcuts']:
                self.file['shortcuts'].append(os.path.abspath(url))
            else:
                dupes.append(url)

        self.__saveJSON()

        if dupes:
            logging.info('Duplicate URL shortcuts tried to be added: %s', ', '.join(dupes))

        return dupes
    
    def removeTool(self, *urls: str) -> None:
        for url in urls:
            if url in self.file['shortcuts']:
                urlToBeDeleted = os.path.abspath(url)
                logging.info('External tool at %s has been deleted', urlToBeDeleted)
                self.file['shortcuts'].remove(urlToBeDeleted)
        
        self.__saveJSON()
    
    def changeTool(self, old: str, new: str) -> None:
        if old in self.file['shortcuts']:
            logging.info('External tool url has changed from %s to %s', old, new)
            index = self.file['shortcuts'].index(os.path.abspath(old))
            self.file['shortcuts'][index] = os.path.abspath(new)

            self.__saveJSON()
