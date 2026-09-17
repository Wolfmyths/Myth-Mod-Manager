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

        self.protonVerComboBox = qtw.QComboBox(self, editable=False)
        self.refresh_combobox()

        addIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListAdd)
        removeIcon = qtg.QIcon.fromTheme(qtg.QIcon.ThemeIcon.ListRemove)

        protonDirsButtonAdd = qtw.QPushButton(addIcon, "", self)
        protonDirsButtonAdd.pressed.connect(self.addProtonDir)
        protonDirButtonLayout.addWidget(protonDirsButtonAdd)

        protonDirsButtonRemove = qtw.QPushButton(removeIcon, "", self)
        protonDirsButtonRemove.pressed.connect(self.removeProtonDir)
        protonDirButtonLayout.addWidget(protonDirsButtonRemove)

        self.protonDirsModel = QStringListModel(OptionsManager.getProtonDirs(), self)
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
        selected_indexes = self.protonDirsListView.selectedIndexes()

        if len(selected_indexes) <= 0:
            return
        
        stringList = self.protonDirsModel.stringList()

        for text in [x.data(Qt.ItemDataRole.DisplayRole) for x in selected_indexes]:
            text: str
            stringList.remove(text)
        
        self.protonDirsModel.setStringList(stringList)
    
    @Slot()
    def refresh_combobox(self) -> None:
        available_proton_versions = helper.findProtonVersions()
        self.protonVerComboBox.clear()
        self.protonVerComboBox.addItems(available_proton_versions)

        proton_version = OptionsManager.getProtonVersion()

        if not proton_version:
            # Select the latest installed version if the option isn't set
            proton_path = helper.getProtonPath(available_proton_versions[0])
            OptionsManager.setProtonVersion(proton_path)
            proton_version = proton_path
        
        index = self.protonVerComboBox.findText(QFileInfo(proton_version).baseName())

        self.protonVerComboBox.setCurrentIndex(index)
        
    def applyStaticText(self) -> None:
            self.setTitle(qapp.translate("OptionsGeneral", "Proton"))
            self.protonLabel.setText(qapp.translate("OptionsGeneral", "Version:"))
            self.protonDirsLabel.setText(qapp.translate("OptionsGeneral", "Custom Proton Directories:"))

    def isProtonDirsChanged(self) -> bool:
        return self.protonDirsModel.stringList() != OptionsManager.getProtonDirs()