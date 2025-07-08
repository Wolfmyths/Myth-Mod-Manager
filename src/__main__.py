import logging
import os
from datetime import datetime

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QTranslator, QLocale

from src.main_window import MainWindow
from src.save import Save, OptionsManager
from src.profileManager import ProfileManager
from src.toolsData import ToolJSON
from src.widgets.QDialog.gamepathQDialog import GamePathNotFound
from src.constant_vars import VERSION, PROGRAM_NAME, LOGS_PATH, IS_SCRIPT, OLD_EXE, ROOT_PATH, MAX_LOGS, OptionKeys, LANG_FOLDER_PATH
import src.errorChecking as errorChecking
from src.style import StyleManager

def setup_logging() -> None:
    time: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logFileName: str = f'log-{time}.txt'

    logging.basicConfig(
        filename=os.path.join(LOGS_PATH, logFileName),
        filemode='a',
        format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if IS_SCRIPT else logging.INFO
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

    logging.info('\nSTARTING: %s\nVERSION: %s\nEXE PATH: %s', PROGRAM_NAME, VERSION, ROOT_PATH)

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

    # Checking game path
    if not OptionsManager.hasOption(OptionKeys.game_path):
        warning = GamePathNotFound(app)
        warning.exec()

    # Checking neccessary directories
    errorChecking.createModDirs()

    window = MainWindow(app)
    window.show()

    app.exec()
