import logging
import os

import PySide6.QtWidgets as qtw

from src.main_window import MainWindow
from src.save import Save, OptionsManager
from src.widgets.QDialog.gamepathQDialog import GamePathNotFound
from src.constant_vars import VERSION, PROGRAM_NAME, LOG, IS_SCRIPT, OLD_EXE, ROOT_PATH, ICON
import src.errorChecking as errorChecking
from src.style import StyleManager


if __name__ == '__main__':

    import sys

    # Old exe appears after updating
    if os.path.exists(OLD_EXE):
        os.remove(OLD_EXE)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.basicConfig(filename=os.path.join(ROOT_PATH, 'logs', LOG),
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG if IS_SCRIPT else logging.INFO)

    logging.info('\nSTARTING: %s\nVERSION: %s\nEXE PATH: %s', PROGRAM_NAME, VERSION, ROOT_PATH)

    app = qtw.QApplication(sys.argv)

    save = Save()
    optionsManager = OptionsManager()

    app.setStyleSheet(StyleManager().getStyleSheet(optionsManager.getTheme()))

    # Checking game path
    if not errorChecking.validGamePath():

        warning = GamePathNotFound(app)
        warning.exec()

    # Checking neccessary directories
    errorChecking.createModDirs()

    window = MainWindow(app)
    window.show()

    app.exec()
