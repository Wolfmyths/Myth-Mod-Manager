import json
import logging
import os

class JSONParser():
    @staticmethod
    def loadJSON(path: str, fallback: dict = {}) -> dict:
        file: dict = {}

        try:
            file = JSONParser._loadJSON(path)
            
        except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f'{e}')

            with open(path, 'w') as f:
                f.write(json.dumps(fallback))
                file = JSONParser._loadJSON(path)

        finally:    
            return file

    @staticmethod
    def saveJSON(path: str, data: dict) -> None:
        with open(path, 'w') as f:
            f.seek(0)
            f.write(json.dumps(data, indent=2))
            f.truncate()
        
        logging.info('%s has been saved.', os.path.basename(path))
    
    @staticmethod
    def _loadJSON(path: str) -> dict:
        with open(path, 'r') as f:
            return json.loads(f.read())