import platform
import os

import PySide6.QtWidgets as qtw
from PySide6.QtCore import QCoreApplication as qapp, Slot
from typing_extensions import override

import src.helpers.helper as helper
from src.helpers.helper_pathing import Pathing
from src.widgets.qdialog.notice import Notice
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

        self.log.setText(qapp.translate("OptionsMisc", "Open Crash Logs..."))
        self.log.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory used by vanilla Payday 2"))

        self.modLog.setText(qapp.translate("OptionsMisc", "Open Mod Crash Logs..."))
        self.modLog.setToolTip(qapp.translate("OptionsMisc", "Opens the crash log directory that BLT uses"))
    
    @Slot()
    def openCrashLogBLT(self) -> None:
        modPath: str = Pathing.mods()

        helper.startFile(os.path.join(modPath, 'logs'))
    
    @Slot()
    def openCrashLogs(self) -> None:

        if platform.system().startswith('Win'):
            os.startfile(os.path.join('C:', 'Users', os.environ['USERNAME'], 'AppData', 'Local', 'PAYDAY 2'))
        else:
            notice = Notice(
                qapp.translate("OptionsMisc", 'Overkill did not implement a vanilla crash log for linux') + ' :(',
                qapp.translate("OptionsMisc", 'Myth Mod Manager: Vanilla crash logs unsupported')
            )
            notice.exec()
    
    @Slot()
    def startBackupMods(self) -> None:
        
        startFileMover = ProgressWidget(BackupMods())
        startFileMover.exec()