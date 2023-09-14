
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import QTimer

from manager import ModManager
from settings import Options
from profiles import modProfile
from save import OptionsManager

from constant_vars import OPTIONS_WINDOWSIZE_W, OPTIONS_WINDOWSIZE_H, ICON, PROGRAM_NAME, VERSION

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qtw.QApplication) -> None:
        super().__init__()

        self.optionsManager = OptionsManager()

        self.setWindowIcon(qtg.QIcon(ICON))
        self.setWindowTitle(f'{PROGRAM_NAME} {VERSION}')
        self.setMinimumSize(800, 800)
        self.resize(self.optionsManager.getOption(OPTIONS_WINDOWSIZE_W, fallback=800, type=int), self.optionsManager.getOption(OPTIONS_WINDOWSIZE_H, fallback=800, type=int))

        self.app = app

        self.tab = qtw.QTabWidget(self)

        # Placeholder for resizeEvent()
        self.newSize: tuple[int] = None

        self.resizeEventTimeout = QTimer()
        self.resizeEventTimeout.timeout.connect(lambda: self.saveWindowSize(*self.newSize))

        self.manager = ModManager()
        self.profile = modProfile()
        self.options = Options()

        for page in (
                        (self.manager, 'Manager'),
                        (self.profile, 'Profiles'),
                        (self.options, 'Options')
                    ):

            self.tab.addTab(page[0], page[1])

        self.setCentralWidget(self.tab)
    
    def resizeEvent(self, event: qtg.QResizeEvent) -> None:

        qSize = event.size()

        self.newSize = (qSize.width(), qSize.height())

        if not self.resizeEventTimeout.isActive():
            self.resizeEventTimeout.start(1000)

        return super().resizeEvent(event)
    
    def saveWindowSize(self, width: int, height: int) -> None:

        self.resizeEventTimeout.stop()

        width = str(width)
        height = str(height)

        self.optionsManager.setOption(width, OPTIONS_WINDOWSIZE_W)
        self.optionsManager.setOption(height, OPTIONS_WINDOWSIZE_H)
