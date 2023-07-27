
import PySide6.QtWidgets as qtw

from main_window import MainWindow
from save import Save, OptionsManager
from widgets.warningQDialog import GamePathNotFound
from constant_vars import VERSION, PROGRAM_NAME
import errorChecking


if __name__ == '__main__':

    import sys

    app = qtw.QApplication(sys.argv)

    save = Save()
    optionsManager = OptionsManager()

    # If the user agrees to update, the program will shutdown
    if errorChecking.checkUpdate() == 1:
        app.shutdown()

    # Checking game path
    if not errorChecking.validGamePath():
        
        warning = GamePathNotFound(app)
        warning.exec()
    

    window = MainWindow(app)
    window.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
    window.setMinimumSize(800, 800)
    window.show()

    app.exec()