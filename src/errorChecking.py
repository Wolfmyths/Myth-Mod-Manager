import os
import requests

from semantic_version import Version

from save import OptionsManager
from widgets.newUpdateQDialog import updateDetected
from constant_vars import OPTIONS_GAMEPATH, MODS_DISABLED_PATH_DEFAULT, VERSION

def validGamePath() -> bool:
    '''Gets the gamepath from OPTIONS_CONFIG and checks if the paths contains the PAYDAY 2 exe'''

    optionsManager = OptionsManager()

    gamePath = optionsManager.getOption(OPTIONS_GAMEPATH)

    if gamePath is None:
        return False

    return os.path.exists(os.path.join(gamePath, 'payday2_win32_release.exe'))

def validDefaultDisabledModsPath() -> bool:
    '''Returns if the default disabled mods folder path exists'''

    return os.path.exists(MODS_DISABLED_PATH_DEFAULT)

def getFileType(filePath: str) -> str | bool:
    '''
    Returns a string of the file format

    If the path leads to a folder, it will return 'dir'

    If FileNotFoundError is raised, it returns False
    '''

    output = None

    try:

        if os.path.isdir(filePath):

            output = 'dir'

        elif filePath.endswith(('.zip', '.rar')):

            output = 'zip'
        
        else:
            raise FileNotFoundError
        
    except FileNotFoundError:

        output = False
    
    finally:
        return output

def isPrerelease(version: Version) -> bool:
    return len(version.prerelease) != 0

def checkUpdate() -> int:
    '''
    Checks for latest update and returns the result value of the updateDetected() QDialog Widget
    
    If the request.get() raises an exception, return 0
    '''

    try:
        # If the version is a pre-release, then look for latest pre-release updates as well
        if isPrerelease(VERSION):

            data = requests.get('https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases').json()

            latestVersion = Version.coerce(data[0]['tag_name'])
        
        else:

            latestVersion = requests.get('https://api.github.com/repos/Wolfmyths/Myth-Mod-Manager/releases/latest').json()['tag_name']
            latestVersion = Version.coerce(latestVersion)

    except Exception as e:
        print(e)

        return 0
    
    if latestVersion > VERSION:

            notice = updateDetected(latestVersion)
            notice.exec()
            result = notice.result()

    else:

        result = 0

    return result