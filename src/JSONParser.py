import json
import logging
import os

class JSONParser():
    file: dict = None
    def __init__(self, path: str, default: dict = {}) -> None:
        self.path = path
        self.default = default
        try:
            self.loadJSON()
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open(self.path, 'w') as f:
                f.write(json.dumps(default))
            
            self.loadJSON()

    def loadJSON(self) -> None:
        with open(self.path, 'r') as f:
            self.file = json.loads(f.read())

    def saveJSON(self) -> None:
        with open(self.path, 'w') as f:
            f.seek(0)
            f.write(json.dumps(self.file, indent=2))
            f.truncate()
        
        logging.info('%s has been saved.', os.path.basename(self.path))