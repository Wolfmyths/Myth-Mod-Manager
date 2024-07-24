import os
import stat
import logging
import webbrowser
import sys
import subprocess

from semantic_version import Version

from PySide6.QtCore import QCoreApplication as qapp

from src.widgets.QDialog.announcementQDialog import Notice

from src.getPath import Pathing
from src.save import OptionsManager
from src.constant_vars import ModType, OPTIONS_CONFIG

logging.getLogger(__name__)

def openWebPage(link: str) -> bool:
    '''`webbrowser.open_new_tab()` but with some exception handling, returns a bool depending if it failed or not'''

    outcome = webbrowser.open_new_tab(link)

    if not outcome:

        logging.error('Could not open web browser:\n%s', link)

        notice = Notice(qapp.translate("ErrorChecking", 'Could not open to') + f' {link}')
        notice.exec()
    
    return outcome

def createModDirs(optionsPath: str = OPTIONS_CONFIG) -> None:
    path = Pathing(optionsPath)
    disPath = OptionsManager(optionsPath).getDispath()

    for modDir in (path.maps(), path.mod_overrides(), path.mods(), disPath):
        if not os.path.isdir(modDir):
            os.mkdir(modDir)

def isInstalled(mod: str, optionsPath: str = OPTIONS_CONFIG) -> bool:
    '''Checks if the mod is installed on the system'''

    installed = False

    path = Pathing(optionsPath)

    possiblePaths = (path.maps(), path.mod_overrides(), path.mods(), OptionsManager(optionsPath).getDispath())

    for path in possiblePaths:

        if os.path.isdir(os.path.join(path, mod)):
            installed = True
            break

    logging.debug('errorChecking.isInstalled(): %s, %s', mod, installed)
    return installed

def getFileType(filePath: str) -> str | bool:
    '''
    Returns a string of the file format

    If the path leads to a folder, it will return 'dir'

    If FileNotFoundError is raised, it returns False
    '''

    output = False

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

    finally:
        return output

def isPrerelease(version: Version) -> bool:
    return version.prerelease != ()

def isTypeMod(modType: ModType) -> bool:
    return isinstance(modType, ModType)

def permissionCheck(src: str) -> int:
    '''
    Checks if a file has all perms,
    if not it will change them to have the correct perms.

    Returns a code depending on the outcome
    '''

    permission = str(oct(os.stat(src).st_mode))[-3:]

    if int(permission) != 777:
        logging.warning('Permission error found, fixing...')
        os.chmod(src, stat.S_IRWXU)

        result = 0

    else:

        result = 1
    
    return result

def startFile(path: str) -> None:
    '''A cross-platform version of `os.startfile()`'''

    logging.info('Starting program "%s"', path)

    try:
        if not os.path.isabs(path):
            raise Exception(
                qapp.translate("ErrorChecking", 'Please use a full path to the program you are starting.')
            )

        if sys.platform.startswith('win'):
            os.startfile(path)
        else:
            cmd = 'open' if sys.platform == 'darwin' else 'xdg-open'
            returnCode = subprocess.run([cmd, path], shell=True)
            returnCode.check_returncode()

    except Exception as e:
        logging.error('Error in errorChecking.startFile(%s): %s', path, str(e))

        notice = Notice(
            qapp.translate("ErrorChecking", 'Error in') + f' errorChecking.startFile({path}): {e}',
            qapp.translate("ErrorChecking", 'Could not start program')
        )
        notice.exec()
