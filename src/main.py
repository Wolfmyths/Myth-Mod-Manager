import PySide6.QtWidgets as qtw

from main_window import MainWindow
from save import Save, OptionsManager
from widgets.warningQDialog import GamePathNotFound
from constant_vars import VERSION
import errorChecking

##### Notes #####
#
# Make only folders in drop events and create runnable .exe
# Add a are you sure QDialog for deleting files
# 

if __name__ == '__main__':

    import sys

    app = qtw.QApplication(sys.argv)

    save = Save()
    optionsManager = OptionsManager()

    if not errorChecking.validGamePath():
        
        warning = GamePathNotFound(app)
        warning.exec()

    

    window = MainWindow(app)
    window.setWindowTitle(f'Payday 2 Mod Manager {VERSION}')
    window.setMinimumSize(800, 800)
    window.show()

    app.exec()