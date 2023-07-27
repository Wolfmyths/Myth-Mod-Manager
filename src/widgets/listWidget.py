
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QUrl

from widgets.contextMenu import ModContextMenu
from widgets.deleteWarningQDialog import DeleteModConfirmation
import errorChecking
from save import Save, OptionsManager
from fileMover import FileMover
from constant_vars import MOD_ENABLED, MOD_LIST_OBJECT, MOD_OVERRIDE_LIST_OBJECT, TYPE_MODS, TYPE_MODS_OVERRIDE

class ModListWidget(qtw.QListWidget):

    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        self.setSelectionMode(qtw.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setAcceptDrops(True)

        self.contextMenu = ModContextMenu(parent=self)

        self.enable = qtg.QAction('Enable', self)
        self.enable.triggered.connect(lambda: self.setItemEnabled())

        self.disable = qtg.QAction('Disable', self)
        self.disable.triggered.connect(lambda: self.setItemDisabled())

        self.delete = qtg.QAction('Delete Mod', self)
        self.delete.triggered.connect(lambda: self.deleteItem())

        self.contextMenu.addActions((self.enable, self.disable, self.delete))
    
    def setItemDisabled(self) -> None:
        '''Sets one or more mods to be disabled in MOD_CONFIG and in the GUI'''

        # Return if already disabled
        # Uses fallback as False otherwise would result in a NoSectionError
        # A NoSectionError would've been raised anyway if disabled since currentItem().text()...
        # returns the mod name with (disabled) in front of it
        if not self.saveManager.isEnabled(self.currentItem().text()):
            return
        
        if self.isMultipleSelected():

            for item in self.selectedItems():

                self.disableItem(item)
        
        else:

            item = self.item(self.currentRow())

            self.disableItem(item)
    
    def disableItem(self, item: qtw.QListWidgetItem) -> None:
            '''Used for setItemDisabled() to reduce repeated code'''

            modName = item.text()

            self.saveManager[modName][MOD_ENABLED] = 'False'

            self.saveManager.writeData()

            self.setItemNameDisabled(item)

            FileMover().moveToDisabledDir(modName)
    
    def deleteItem(self) -> None:

        warning = DeleteModConfirmation(self)
        warning.exec()

        if not warning.result():
            return

        if self.isMultipleSelected():

            for item in self.selectedItems():

                modName = item.text()

                FileMover().deleteMod(modName)

                self.takeItem(self.row(item))

        else:

            item = self.currentItem()

            modName = item.text()

            FileMover().deleteMod(modName)

            self.takeItem(self.row(item))
    
    def setItemNameDisabled(self, item: qtw.QListWidgetItem) -> None:

        item.setText(f'{item.text()} (disabled)')
    
    def setItemEnabled(self) -> None:
        '''Sets one or more mods to be enabled in MOD_CONFIG and in the GUI'''

        if self.isMultipleSelected():

            for item in self.selectedItems():

                self.enableItem(item)

        else:

            item = self.item(self.currentRow())

            self.enableItem(item)

        self.saveManager.writeData()
    
    def enableItem(self, item: qtw.QListWidgetItem) -> None:

        modName = item.text().replace(' (disabled)', '')

        self.saveManager[modName][MOD_ENABLED] = 'True'

        item.setText(modName)

        FileMover().moveToEnableModDir(modName)
    
    def isMultipleSelected(self) -> bool:
        return len(self.selectedItems()) > 1

    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:

        if event.button() == qt.MouseButton.RightButton:

            self.contextMenu.show()

        return super().mousePressEvent(event)
    
    def dragEnterEvent(self, event: qtg.QDragEnterEvent) -> None:
        
        if event.mimeData().hasUrls():

            event.accept()

        else:
            event.ignore()
    
    def dragMoveEvent(self, event: qtg.QDragMoveEvent) -> None:
        
        if event.mimeData().hasUrls():

            event.setDropAction(qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event: qtg.QDropEvent) -> None:

        if event.mimeData().hasUrls():

            conversion = {MOD_LIST_OBJECT : TYPE_MODS, MOD_OVERRIDE_LIST_OBJECT : TYPE_MODS_OVERRIDE}
            listName = self.objectName()

            event.setDropAction(qt.DropAction.MoveAction)

            for mod in event.mimeData().urls():

                filepath = mod.toLocalFile()

                if errorChecking.getFileType(filepath) == 'dir':

                    filename = filepath.split('/')[-1]
                    
                    # Moving file to the correct dir
                    FileMover().changeModType(filepath, ChosenDir = listName)

                    # Adding mod to config
                    self.saveManager.addMods((filename, conversion[listName]))

                    # Adding file to the list
                    self.addItem(filename)

                    # Sorting items
                    self.sortItems()
                
                else:
                    event.ignore()
                    return

            event.accept()
        else:
            event.ignore()