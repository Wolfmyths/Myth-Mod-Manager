
import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from widgets.contextMenu import ModContextMenu
from widgets.deleteWarningQDialog import DeleteModConfirmation
from widgets.newModQDialog import newModLocation
import errorChecking
from save import Save, OptionsManager
from fileMover import FileMover
from constant_vars import MOD_ENABLED, TYPE_MODS, TYPE_MODS_OVERRIDE

class ModListWidget(qtw.QTableWidget):

    def __init__(self) -> None:
        super().__init__()

        self.saveManager = Save()
        self.optionsManager = OptionsManager()

        self.setSelectionMode(qtw.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(qtw.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAcceptDrops(True)

        self.setColumnCount(3)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 100)

        self.setHorizontalHeaderLabels(('Name', 'Type', 'Enabled'))

        self.sortState = {'col' : 0, 'ascending': True}

        self.horizontalHeader().sectionClicked.connect(lambda x: self.changeSortState(x))

        self.horizontalHeader().setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.Interactive)
        self.horizontalHeader().setSectionResizeMode(2, qtw.QHeaderView.ResizeMode.Interactive)

        self.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalHeader().hide()

        self.contextMenu = ModContextMenu(parent=self)

        self.enable = qtg.QAction('Enable', self)
        self.enable.triggered.connect(lambda: self.setItemEnabled())

        self.disable = qtg.QAction('Disable', self)
        self.disable.triggered.connect(lambda: self.setItemDisabled())

        self.delete = qtg.QAction('Delete Mod', self)
        self.delete.triggered.connect(lambda: self.deleteItem())

        self.contextMenu.addActions((self.enable, self.disable, self.delete))
    
    def getEnabledItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 2)
    
    def getNameItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 0)
    
    def getTypeItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 1)
    
    def getModTypeCount(self, modType: str) -> int | None:
        '''
        Returns the modtype count in the table,
        if an invalid parameter is passed then return None
        '''

        if modType in (TYPE_MODS, TYPE_MODS_OVERRIDE):
            return len(self.findItems(modType, qt.MatchFlag.MatchExactly))
    
    def changeSortState(self, header) -> None:

        if self.sortState['col'] == header:

            self.sortState['ascending'] = not self.sortState['ascending']

        self.sortState['col'] = header

        self.sort()
    
    def sort(self):

        if self.sortState['ascending']:

            sortType = qt.SortOrder.AscendingOrder
        else:
            sortType = qt.SortOrder.DescendingOrder


        self.sortItems(self.sortState['col'], sortType)
    
    def addMod(self, **kwargs: str | bool) -> None:
        '''
        Adds a new mod to the table (Not in the save manager)

        Accepted kwargs:

        + name : str
        + type : str
        + enabled : bool

        If there is any other kwarg, then it will return
        '''

        self.insertRow(self.rowCount())

        for key, value in kwargs.items():

            match key:

                case 'name':
                    self.setItem(self.rowCount() - 1, 0, qtw.QTableWidgetItem(value))

                case 'type':
                    self.setItem(self.rowCount() - 1, 1, qtw.QTableWidgetItem(value))

                case 'enabled': # The key to this value should be a boolean

                    value = 'Enabled' if value else 'Disabled'
                    self.setItem(self.rowCount() - 1, 2, qtw.QTableWidgetItem(value))

                case _:
                    continue
    
    def setItemDisabled(self) -> None:
        '''Sets one or more mods to be disabled in MOD_CONFIG and in the GUI'''

        # Return if already disabled
        # Uses fallback as False otherwise would result in a NoSectionError
        # A NoSectionError would've been raised anyway if disabled since currentItem().text()...
        # returns the mod name with (disabled) in front of it

        items = self.selectedItems()

        for i in range(0, len(items), self.columnCount()):

            row = items[i].row()

            modName = self.getNameItem(row).text()

            if self.saveManager.isEnabled(modName):

                self.saveManager[modName][MOD_ENABLED] = 'False'

                self.saveManager.writeData()

                self.getEnabledItem(row).setText('Disabled')

                FileMover().moveToDisabledDir(modName)
    
    def deleteItem(self) -> None:

        warning = DeleteModConfirmation(self)
        warning.exec()

        if warning.result():

            items = self.selectedItems()

            for i in range(0, len(items), self.columnCount()):

                mod = items[i]

                modName = mod.text()

                row = items[i].row()

                FileMover().deleteMod(modName)

                self.removeRow(row)
    
    def setItemEnabled(self) -> None:
        '''Sets one or more mods to be enabled in MOD_CONFIG and in the GUI'''

        items = self.selectedItems()

        for i in range(0, len(items), self.columnCount()):

            row = items[i].row()

            modName = self.getNameItem(row).text()

            self.saveManager[modName][MOD_ENABLED] = 'True'

            FileMover().moveToEnableModDir(modName)

            self.getEnabledItem(row).setText('Enabled')

        self.saveManager.writeData()
    
    # This isn't used anywhere, might be removed
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

        '''
        All cases except where files can be moved should end in `return event.ignore()`
        to prevent the file from automatically being put into the recycling bin

        The only exception to this is when the file being dropped is a regular folder
        '''

        if event.mimeData().hasUrls():            

            event.setDropAction(qt.DropAction.MoveAction)

            urls = event.mimeData().urls()

            for mod in urls:

                filepath = mod.toLocalFile()

                fileType = errorChecking.getFileType(filepath)
                print(fileType)

                if fileType == 'dir' or fileType == 'zip':

                    filename = filepath.split('/')[-1]

                    # Pop up asking what directory it belongs to
                    popup = newModLocation(filename)
                    popup.exec()

                    type = popup.type

                    if type is not None and fileType == 'dir':
                        print('passed type is not none and is dir check')
                    
                        # Moving file to the correct dir
                        FileMover().changeModType(filepath, ChosenDir = type)
                        print('Should be in mod_overrides now')

                        # Adding mod to config
                        self.saveManager.addMods((filename, type))

                        # Adding file to the table
                        self.addMod(name=filename, type=type, enabled=True)

                        self.sort()

                        event.accept()
                        return
                    
                    elif type is not None and fileType == 'zip':
                        
                        # Outputs a tuple, please see unZipMod documentation
                        outcome = FileMover().unZipMod(filepath, type)

                        if outcome[0] != 2:

                            fileName = outcome[1]

                            self.saveManager.addMods((fileName, type))

                            self.addMod(name=fileName, type=type, enabled=True)

                    else:
                        event.ignore()
                        return
                    
                    self.sort()
                
                else:
                    
                    continue

            event.ignore()

        else:
            event.ignore()