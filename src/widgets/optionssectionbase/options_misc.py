import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, QDir, Slot
from typing_extensions import override

from src.constant_vars import IS_WINDOWS
import src.helpers.helper as helper
from src.helpers.helper_pathing import Pathing
from src.helpers.options_manager import OptionsManager
from src.widgets.qdialog.progress_widget import ProgressWidget
from src.widgets.optionssectionbase.option_section_base import OptionsSectionBase
from src.objects.backup_mods import BackupMods

class OptionsMisc(OptionsSectionBase):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent= parent)

        layout = qtw.QVBoxLayout()
        
        self.miscGroup = qtw.QGroupBox(self)

        miscGroupLayout = qtw.QVBoxLayout()

        self.backupMods = qtw.QPushButton(self)
        self.backupMods.clicked.connect(self.startBackupMods)

        self.log = qtw.QPushButton(self)
        self.log.clicked.connect(self.openCrashLogs)

        self.modLog = qtw.QPushButton(self)
        self.modLog.clicked.connect(self.openCrashLogBLT)

        for widget in (self.backupMods, self.log, self.modLog):
            miscGroupLayout.addWidget(widget)
        
        self.miscGroup.setLayout(miscGroupLayout)

        for widget in (self.miscGroup, ):
            layout.addWidget(widget)

        self.applyStaticText()

        self.setLayout(layout)
    
    @override
    def applyStaticText(self) -> None:
        self.miscGroup.setTitle(qapp.translate("OptionsMisc", "Misc"))

        self.backupMods.setText(qapp.translate("OptionsMisc", "Backup Mods"))
        self.backupMods.setToolTip(qapp.translate("OptionsMisc", "Copies and compresses all of your mods to MMM's installation folder"))

        self.log.setText(qapp.translate("OptionsMisc", "Open Crash Logs and Save Data..."))
        self.log.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory used by vanilla Payday 2"))

        self.modLog.setText(qapp.translate("OptionsMisc", "Open Mod Crash Logs..."))
        self.modLog.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory that BLT uses"))
    
    @Slot()
    def openCrashLogBLT(self) -> None:
        modPath: str = Pathing.mods()

        helper.startFile(os.path.join(modPath, 'logs'))
    
    @Slot()
    def openCrashLogs(self) -> None:

        if IS_WINDOWS:
            os.startfile(f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Local\\PAYDAY 2")
        else:
            compatdata_path = QDir(f'{OptionsManager.getGamepath()}/../../compatdata').canonicalPath()
            helper.startFile(
                f"{compatdata_path}/218620/pfx/drive_c/users/steamuser/AppData/Local/PAYDAY 2")
    
    @Slot()
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()