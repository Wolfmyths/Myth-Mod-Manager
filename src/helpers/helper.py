import os
import stat
import logging
import webbrowser

from semantic_version import Version

from PySide6.QtCore import QCoreApplication as qapp, Slot, QUrl, QRegularExpression, QRegularExpressionMatchIterator
from PySide6.QtGui import QDesktopServices

from src.widgets.qdialog.notice import Notice

from src.helpers.helper_pathing import Pathing
from src.helpers.options_manager import OptionsManager
from src.constant_vars import ModType
logging.getLogger(__name__)

@Slot(str)
def openWebPage(link: str) -> bool:
    '''`webbrowser.open_new_tab()` but with some exception handling, returns a bool depending if it failed or not'''

    outcome: bool = webbrowser.open_new_tab(link)

    if not outcome:

        logging.error('Could not open web browser:\n%s', link)

        notice = Notice(qapp.translate("ErrorChecking", 'Could not open to') + f' {link}')
        notice.exec()
    
    return outcome

def createModDirs() -> None:
    disPath: str = OptionsManager.getDispath()

    for modDir in (Pathing.maps(), Pathing.mod_overrides(), Pathing.mods(), disPath):
        if not os.path.isdir(modDir):
            os.mkdir(modDir)

def isInstalled(mod: str) -> bool:
    '''Checks if the mod is installed on the system'''

    installed = False

    possiblePaths: tuple[str, str, str, str] = (
        Pathing.maps(),
        Pathing.mod_overrides(),
        Pathing.mods(),
        OptionsManager.getDispath()
    )

    for path in possiblePaths:

        if os.path.isdir(os.path.join(path, mod)):
            installed = True
            break

    logging.debug('helper.isInstalled(): %s, %s', mod, installed)
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

    permission: str = str(oct(os.stat(src).st_mode))[-3:]

    if int(permission) != 777:
        logging.warning('Permission error found, fixing...')
        os.chmod(src, stat.S_IRWXU)

        result = 0

    else:

        result = 1
    
    return result

def launchParamsToList(params: str = '') -> list[str]:
    '''
    Returns launch parameters in a list rather than a single string

    If not given an arg, will use the launch parameters from the user's settings
    '''

    if not params:
        params = OptionsManager.getLaunchParameters()

    regex = QRegularExpression(r'(-\w+(?: [^-]\S*)*)')
    regexResult: QRegularExpressionMatchIterator = regex.globalMatch(params)

    finalResult: list[str] = []
    while regexResult.hasNext():
        finalResult.append(regexResult.next().captured(1))
    
    return finalResult

@Slot(str)
def startFile(path: str) -> None:
    '''A cross-platform version of `os.startfile()`'''

    logging.info('Starting program "%s"', path)

    try:
        if not os.path.isabs(path):
            raise Exception(
                qapp.translate("ErrorChecking", 'Please use a full path to the program you are starting.')
            )

        returnCode: bool = QDesktopServices.openUrl(QUrl(f"file:///{path}"))
        if not returnCode:
            raise Exception(
                qapp.translate("ErrorChecking", "Someting went wrong opening with given path")
            )

    except Exception as e:
        logging.error('Error in errorChecking.startFile(%s): %s', path, str(e))

        notice = Notice(
            qapp.translate("ErrorChecking", 'Error in') + f' errorChecking.startFile({path}): {e}',
            qapp.translate("ErrorChecking", 'Could not start program')
        )
        notice.exec()
