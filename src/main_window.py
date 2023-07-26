
import PySide6.QtWidgets as qtw

from manager import ModManager
from settings import Options

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qtw.QApplication) -> None:
        super().__init__()

        self.app = app

        self.tab = qtw.QTabWidget(self)

        self.manager = ModManager()
        self.options = Options()

        for page in (
                        (self.manager, 'Manager'),
                        (self.options, 'Options')
                    ):

            self.tab.addTab(page[0], page[1])

        self.setCentralWidget(self.tab)
        