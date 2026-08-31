import logging
import os
from datetime import datetime

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QTranslator, QLocale, QFileInfo

from src.widgets.qwidget.main_window import MainWindow
from src.helpers.options_manager import OptionsManager
from src.helpers.profile_manager import ProfileManager
from src.helpers.save_manager import Save
from src.helpers.tools_manager import ToolJSON
from src.widgets.qdialog.gamepath_not_found import GamePathNotFound
from src.constant_vars import VERSION, PROGRAM_NAME, LOGS_PATH, IS_DEBUG, OLD_EXE, ROOT_PATH, MAX_LOGS, LANG_FOLDER_PATH
import src.helpers.helper as helper
from src.helpers.style import StyleManager

def setup_logging() -> None:
    time: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logFileName: str = f'log-{time}.txt'

    logging.basicConfig(
        filename=os.path.join(LOGS_PATH, logFileName),
        filemode='a',
        format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if IS_DEBUG else logging.INFO
    )

    # Delete extra log files
    logs: list[str] = os.listdir(LOGS_PATH)
    logs_count: int = len(logs)

    if logs_count > MAX_LOGS:
        for i in range(logs_count - MAX_LOGS + 1):
            logging.info("Too many logs, deleting %s", logs[i])
            os.remove(os.path.join(LOGS_PATH, logs[i]))

if __name__ == '__main__':

    import sys

    # Old exe appears after updating
    if os.path.exists(OLD_EXE):
        os.remove(OLD_EXE)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    setup_logging()

    logging.info('\nSTARTING: %s\nVERSION: %s\nEXE PATH: %s', PROGRAM_NAME, VERSION.toString(), ROOT_PATH)

    app = qtw.QApplication(sys.argv)
    QLocale.setDefault(QLocale.Language.English)

    # Initialize Static Classes
    OptionsManager()
    Save()
    ToolJSON()
    ProfileManager()

    translator = QTranslator(app)
    path: str = os.path.join(LANG_FOLDER_PATH, OptionsManager.getLang() + '.qm')
    if not translator.load(path):
       logging.error('Translator failed to load: %s', os.path.basename(path))
    else:
        app.installTranslator(translator)
        logging.info('Loaded language: %s', translator.language())

    app.setStyleSheet(StyleManager().getStyleSheet(OptionsManager.getTheme()))

    logging.info("Gamepath: %s", OptionsManager.getGameExecuteable())
    
    # Checking game path
    gameEXE = QFileInfo(OptionsManager.getGameExecuteable())
    if not gameEXE.isExecutable() or not gameEXE.isFile():
        warning = GamePathNotFound()
        warning.exec()

    # Checking neccessary directories
    helper.createModDirs()

    window = MainWindow(app)
    window.show()

    app.exec()
