import platform
import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot, QProcess, QProcessEnvironment
import PySide6.QtGui as qtg
from typing_extensions import override

from src.widgets.qtable.mod_list_widget import ModListWidget
from src.widgets.qdialog.notice import Notice
from src.helpers.options_manager import OptionsManager
import src.helpers.helper as helper
from src.constant_vars import ModType, STEAM

class ModManager(qtw.QWidget):

    def __init__(self) -> None:
        super().__init__()

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
        args: list[str] = OptionsManager.getLaunchParametersList()

        #print(f"Launching PAYDAY 2\nargs: {args}\ngame path: {gamePath}")

        try:
            game_exe_path = OptionsManager.getGameExecuteable()

            success: int
            exit_code: int

            process = QProcess()

            if platform.system().startswith("Win"):
                success, exit_code = process.startDetached(game_exe_path, args, gamePath)
            else:
                proton_ver = OptionsManager.getProtonVersion()
                STEAM_COMPAT_DATA_PATH = f"{STEAM}/steamapps/compatdata/218620"
                proton_path = f"{proton_ver}/proton"
                
                env = QProcessEnvironment()
                env.insert("STEAM_COMPAT_DATA_PATH", STEAM_COMPAT_DATA_PATH)
                env.insert("STEAM_COMPAT_CLIENT_INSTALL_PATH", STEAM)

                process.setProcessEnvironment(env)
                process.setArguments(
                    [f"run {game_exe_path}"] + args)
                process.setWorkingDirectory(gamePath)
                process.setProgram(proton_path)
                
                success, exit_code = process.startDetached()

            if not success:
                raise Exception(
                    qapp.translate("ModManager", "Exit code:") + f' {exit_code}\n{process.errorString()}'
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
