import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt, QStringListModel, QCoreApplication as qapp, QFileInfo, Slot

from src.helpers.options_manager import OptionsManager
from src.helpers import helper

class ProtonSettingsGroupBox(qtw.QGroupBox):
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)

        protonLayout = qtw.QVBoxLayout()
        protonDirButtonLayout = qtw.QHBoxLayout()
        protonDirButtonLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        available_proton_versions: list[str] = ["N/A"]
        if not OptionsManager.getProtonVersion():
            # Select the latest installed version if the option isn't set
            available_proton_versions = helper.findProtonVersions()
            proton_path = helper.getProtonPath(available_proton_versions[0])
            OptionsManager.setProtonVersion(proton_path)

        self.protonVerComboBox = qtw.QComboBox(self, editable=False)
        self.protonVerComboBox.addItems(available_proton_versions)
        self.protonVerComboBox.currentTextChanged.connect(self.protonVerChanged)

        addIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListAdd)
        removeIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListRemove)

        protonDirsButtonAdd = qtw.QPushButton(addIcon, "", self)
        protonDirsButtonAdd.pressed.connect(self.addProtonDir)
        protonDirButtonLayout.addWidget(protonDirsButtonAdd)

        protonDirsButtonRemove = qtw.QPushButton(removeIcon, "", self)
        protonDirsButtonRemove.pressed.connect(self.removeProtonDir)
        protonDirButtonLayout.addWidget(protonDirsButtonRemove)

        self.protonDirsModel = QStringListModel(OptionsManager.getProtonDirs(), self)
        self.protonDirsModel.dataChanged.connect(self.protonDirsDataChanged)
        self.protonDirsListView = qtw.QListView(
            self, 
            viewMode=qtw.QListView.ViewMode.ListMode,
            flow=qtw.QListView.Flow.TopToBottom)
        self.protonDirsListView.setEditTriggers(qtw.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.protonDirsListView.setModel(self.protonDirsModel)

        self.protonLabel = qtw.QLabel(self)
        self.protonDirsLabel = qtw.QLabel(self)

        # Setting rows for Proton Sub Section Layout
        protonLayout.addWidget(self.protonLabel)
        protonLayout.addWidget(self.protonVerComboBox)
        protonLayout.addWidget(self.protonDirsLabel)
        protonLayout.addLayout(protonDirButtonLayout)
        protonLayout.addWidget(self.protonDirsListView)
        self.setLayout(protonLayout)

        self.applyStaticText()

    @Slot()
    def addProtonDir(self) -> None:
        url = qtw.QFileDialog.getExistingDirectoryUrl(
            self,
            caption=qapp.translate('OptionsGeneral', 'Select a Location Where Proton Versions Are Stored')
        ).toLocalFile()

        if not QFileInfo(url).exists():
            return
        
        self.protonDirsModel.setStringList(self.protonDirsModel.stringList() + [url])

    @Slot()
    def removeProtonDir(self) -> None:
        for qmodelindex in self.protonDirsListView.selectedIndexes():
            self.protonDirsModel.removeRow(qmodelindex.row())
    
    def applyStaticText(self) -> None:
            self.setTitle(qapp.translate("OptionsGeneral", "Proton"))
            self.protonLabel.setText(qapp.translate("OptionsGeneral", "Version:"))
            self.protonDirsLabel.setText(qapp.translate("OptionsGeneral", "Custom Proton Directories:"))

    def isProtonDirsChanged(self) -> bool:
        return self.protonDirsModel.stringList() != OptionsManager.getProtonDirs()