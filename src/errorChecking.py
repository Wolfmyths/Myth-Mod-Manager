import os
import stat
import logging
import webbrowser

from semantic_version import Version

from src.widgets.QDialog.announcementQDialog import Notice

from src.getPath import Pathing
from src.save import OptionsManager
from src.constant_vars import OPTIONS_GAMEPATH, MODS_DISABLED_PATH_DEFAULT, OPTIONS_DISPATH, OPTIONS_SECTION, ModType

logging.getLogger(__name__)

def openWebPage(link: str) -> None:
        '''`webbrowser.open_new_tab()` but with some exception handling'''
        try:
            webbrowser.open_new_tab(link)
        except Exception as e:

            logging.error('Could not open web browser:\n%s', str(e))

            notice = Notice(f'Could not connect to {link}:\n{e}', 'Error:')
            notice.exec()

def validGamePath() -> bool:
    '''Gets the gamepath from OPTIONS_CONFIG and checks if the paths contains the PAYDAY 2 exe'''

    optionsManager = OptionsManager()

    gamePath = optionsManager.getOption(OPTIONS_GAMEPATH)

    if gamePath is None:

        logging.warning('There is no gamepath')
        return False

    else:
        logging.info('Gamepath: %s', gamePath)

    return 'payday2_win32_release.exe' in os.listdir(gamePath)

def createModDirs() -> None:
    path = Pathing()

    for modDir in (path.maps(), path.mod_overrides(), path.mods()):
        if not os.path.isdir(modDir):
            os.mkdir(modDir)

def isInstalled(mod: str) -> bool:
    '''Checks if the mod is installed on the system'''

    installed = False

    path = Pathing()

    possiblePaths = (path.maps(), path.mod_overrides(), path.mods(), OptionsManager().getOption(OPTIONS_DISPATH, MODS_DISABLED_PATH_DEFAULT, str))

    for path in possiblePaths:

        if mod in os.listdir(path):
            installed = True
            break

    logging.debug('errorChecking.isInstalled(): %s, %s', mod, installed)
    return installed

def createDisabledModFolder() -> None:
    '''
    Checks if the OPTIONS_DISPATH path exists, if not, it will try to create a directory there.

    If that fails then it will make a directory at the default location if it isn't already there.

    During an exception it will also overwrite the current OPTIONS_DISPATH with the default value
    to get rid of a faulty path.
    '''

    optionsManager = OptionsManager()

    path = optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

    if not os.path.isdir(path):
        logging.debug('Disabled Mod Folder does not exist')

        try:

            os.mkdir(path)

        except (FileNotFoundError):

            logging.warning('The following path for disabled mods was not found: %s\nUsing default path: %s', path, MODS_DISABLED_PATH_DEFAULT)

            optionsManager[OPTIONS_SECTION][OPTIONS_DISPATH] = MODS_DISABLED_PATH_DEFAULT

            optionsManager.writeData()

            if not os.path.isdir(MODS_DISABLED_PATH_DEFAULT):
                logging.warning('Default disabled mod path was not found, creating new one...')
                
                os.mkdir(MODS_DISABLED_PATH_DEFAULT)

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

        elif filePath.endswith(('.zip', '.rar', '.7z')):

            output = 'zip'
        
        else:
            raise FileNotFoundError
        
        logging.debug('File name: %s\nType: %s', filePath.split('/')[-1], output)
        
    except FileNotFoundError:
        logging.warning('The file extension not valid and will be ignored: %s', filePath.split('/')[-1])

        output = False

    finally:
        return output

def isPrerelease(version: Version) -> bool:
    return len(version.prerelease) != 0

def isTypeMod(type: ModType) -> bool:
    return type.value in ModType.all_types()

def permissionCheck(src: str) -> int:
    '''
    Checks if a file has all perms,
    if not it will change them to have the correct perms.

    Returns a code depending on the outcome
    '''

    permission = str(oct(os.stat(src).st_mode))[-3:]

    if int(permission) != 777:
        logging.info('Permission error found, fixing...')
        os.chmod(src, stat.S_IRWXU)

        result = 0

    else:

        result = 1
    
    return result