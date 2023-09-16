
import logging
import os

import PySide6.QtWidgets as qtw

from main_window import MainWindow
from save import Save, OptionsManager
from widgets.QDialog.gamepathQDialog import GamePathNotFound
from constant_vars import VERSION, PROGRAM_NAME, LOG, IS_SCRIPT, OPTIONS_THEME, LIGHT, OLD_EXE
import errorChecking
from style import StyleManager


if __name__ == '__main__':

    import sys

    # Old exe appears after updating
    if os.path.exists(OLD_EXE):
        os.remove(OLD_EXE)

    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging.basicConfig(filename=f'logs/{LOG}',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG if IS_SCRIPT else logging.INFO)

    logging.info('STARTING %s, VERSION %s', PROGRAM_NAME, VERSION)

    app = qtw.QApplication(sys.argv)

    save = Save()
    optionsManager = OptionsManager()

    app.setStyleSheet(StyleManager().getStyleSheet(optionsManager.getOption(OPTIONS_THEME, LIGHT)))

    # If there's an update a QDialog will pop up
    # When the user successfully updates the app will shutdown
    update = errorChecking.checkUpdate()
    if update == 1:
        app.shutdown()

    # Checking game path
    if not errorChecking.validGamePath():

        warning = GamePathNotFound(app)
        warning.exec()

    window = MainWindow(app)
    window.show()

    app.exec()
