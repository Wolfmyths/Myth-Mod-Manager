import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw

from manager import ModManager
from settings import Options
from profiles import modProfile
from widgets.aboutQWidget import About
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

        self.manager = ModManager()
        self.profile = modProfile()
        self.options = Options()
        self.about = About()

        self.options.ignoredModsListWidget.itemsRemoved.connect(self.manager.modsTable.refreshMods)
        self.options.colorThemeDark.clicked.connect(self.manager.modsTable.swapIcons)
        self.options.colorThemeLight.clicked.connect(self.manager.modsTable.swapIcons)

        self.options.colorThemeDark.clicked.connect(self.about.updateIcons)
        self.options.colorThemeLight.clicked.connect(self.about.updateIcons)

        for page in (
                        (self.manager, 'Manager'),
                        (self.profile, 'Profiles'),
                        (self.options, 'Options'),
                        (self.about, 'About')
                    ):

            self.tab.addTab(page[0], page[1])

        self.setCentralWidget(self.tab)
    
    def close(self) -> bool:
        self.optionsManager.setOption(self.width(), OPTIONS_WINDOWSIZE_W)
        self.optionsManager.setOption(self.height(), OPTIONS_WINDOWSIZE_H)

        return super().close()
