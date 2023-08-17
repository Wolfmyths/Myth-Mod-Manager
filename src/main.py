
import logging
import os

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

from main_window import MainWindow
from save import Save, OptionsManager
from widgets.gamepathQDialog import GamePathNotFound
from constant_vars import VERSION, PROGRAM_NAME, LOG, IS_SCRIPT, OPTIONS_THEME, LIGHT, ICON
import errorChecking
from style import StyleManager


if __name__ == '__main__':

    import sys

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

    # If the user agrees to update, the program will shutdown
    if errorChecking.checkUpdate() == 1:
        app.shutdown()

    # Checking game path
    if not errorChecking.validGamePath():

        warning = GamePathNotFound(app)
        warning.exec()

    window = MainWindow(app)
    window.setWindowIcon(qtg.QIcon(ICON))
    window.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
    window.setMinimumSize(800, 800)
    window.show()

    app.exec()