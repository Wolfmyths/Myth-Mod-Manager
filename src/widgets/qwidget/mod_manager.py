import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QStandardPaths, Qt as qt, QCoreApplication as qapp, Slot, QProcess
import PySide6.QtGui as qtg
from typing_extensions import override

from src.widgets.qtable.mod_list_widget import ModListWidget
from src.widgets.qdialog.notice import Notice
from src.helpers.options_manager import OptionsManager
import src.helpers.helper as helper
from src.constant_vars import IS_WINDOWS, ModType

class ModManager(qtw.QWidget):

    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)

        self.setObjectName('manager')

        layout = qtw.QVBoxLayout()

        self.setAcceptDrops(True)

        self.refresh = qtw.QPushButton(self)

        self.openGameDir = qtw.QPushButton(self)

        self.startGame = qtw.QPushButton(self)

        modLabelLayout = qtw.QHBoxLayout()
        modLabelLayout.setSpacing(100)
        modLabelLayout.setAlignment(qt.AlignmentFlag.AlignHCenter)

        self.labelFrame = qtw.QFrame()

        self.totalModsLabel = qtw.QLabel(self)

        self.modsLabel = qtw.QLabel(self)

        self.overrideLabel = qtw.QLabel(self)

        self.mapsLabel = qtw.QLabel(self)

        for widget in (self.totalModsLabel, self.modsLabel, self.overrideLabel, self.mapsLabel):
            modLabelLayout.addWidget(widget)

        self.labelFrame.setLayout(modLabelLayout)

        self.search = qtw.QLineEdit()

        self.modsTable = ModListWidget()

        self.modsTable.refreshMods()

        for widget in (self.refresh, self.openGameDir, self.startGame, self.labelFrame, self.search, self.modsTable):
            layout.addWidget(widget)
        
        self.applyStaticText()
        self.updateModCount()

        self.refresh.clicked.connect(self.onRefreshClicked)
        self.openGameDir.clicked.connect(self.onOpenGameDirClicked)
        self.startGame.clicked.connect(self.startPayday)
        self.search.textChanged.connect(self.modsTable.search)
        self.modsTable.itemChanged.connect(self.updateModCount)

        # Shortcuts
        self.selectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+A"), self)
        self.selectAllShortCut.activated.connect(self.modsTable.selectAll)

        self.deselectAllShortCut = qtg.QShortcut(qtg.QKeySequence("Ctrl+D"), self)
        self.deselectAllShortCut.activated.connect(self.deselectAllShortcut)

        self.setLayout(layout)
    
    @Slot()
    def onRefreshClicked(self) -> None:
        self.modsTable.refreshMods(True)
    
    @Slot()
    def onOpenGameDirClicked(self) -> None:
        helper.startFile(OptionsManager.getGamepath())

    def applyStaticText(self) -> None:
        self.refresh.setText(qapp.translate("ModManager", "Refresh Mods"))
        self.openGameDir.setText(qapp.translate("ModManager", 'Open Game Directory'))
        self.startGame.setText(qapp.translate("ModManager", 'Start PAYDAY 2'))
        self.search.setPlaceholderText(qapp.translate("ModManager", 'Search... use "tag:" with no spaces to search for tags, use a comma "," to seperate tags'))

    @Slot()
    def updateModCount(self) -> None:

        self.totalModsLabel.setText(qapp.translate("ModManager", 'Total Mods') + f': {self.modsTable.rowCount()}')

        self.modsLabel.setText(f'Mods: {self.modsTable.getModTypeCount(ModType.mods)}')

        self.overrideLabel.setText(f'Mod_Overrides: {self.modsTable.getModTypeCount(ModType.mods_override)}')

        self.mapsLabel.setText(f'Maps: {self.modsTable.getModTypeCount(ModType.maps)}')

    @Slot()
    def startPayday(self) -> None:

        gamePath: str = OptionsManager.getGamepath()
        args: list[str] = QProcess.splitCommand(OptionsManager.getLaunchParameters())

        logging.info(f"Launching PAYDAY 2\nargs: {args}\ngame path: {gamePath}")

        try:
            game_exe_path = OptionsManager.getGameExecuteable()

            process = QProcess()
            # Use steam command if on linux
            steam_path: str = QStandardPaths.findExecutable("steam") if IS_WINDOWS else "steam"
            is_game_not_from_steam = helper.isGameNotFromSteam()

            # Steam executable could not be found
            if not steam_path and not is_game_not_from_steam:
                logging.warning(
                    "Game is steam installation, but steam exe path could not be found! Starting from the executable itself...")

            # Use steam to launch
            if not is_game_not_from_steam and steam_path:
                process.setProgram(steam_path)
                process.setArguments(["-applaunch", "218620"] + args)
            else:
                # Start from the exe itself
                process.setProgram(game_exe_path)
                process.setArguments(args)
                process.setWorkingDirectory(gamePath)
            
            # PySide return type hint is wrong with QProcess.startDetatched()???
            # Returns bool as said online, does not return a Tuple[bool, int]
            # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QProcess.html
            success: bool = process.startDetached() # pyright: ignore[reportAssignmentType]

            if not success:
                raise Exception(
                    qapp.translate("ModManager", "Exit code:") + f' {process.exitCode()}\n{process.errorString()}'
                )

        except Exception as e:
            logging.error('An error occured trying to start PAYDAY 2:\n%s', str(e))

            notice = Notice(
                qapp.translate("ModManager", 'An error occured trying to start PAYDAY 2') + f':\n{e}',
                qapp.translate("ModManager", 'Could not start PAYDAY 2 from MMM'))
            notice.exec()

    @Slot()
    def deselectAllShortcut(self) -> None:
        selectedItems: list[qtw.QTableWidgetItem] = self.modsTable.selectedItems()
        if selectedItems:
            for item in selectedItems:
                item.setSelected(False)

    @override
    def keyPressEvent(self, event: qtg.QKeyEvent) -> None:
        if event.key() == qt.Key.Key_Delete and self.modsTable.selectedItems():
            self.modsTable.deleteItem()
        return super().keyPressEvent(event)
