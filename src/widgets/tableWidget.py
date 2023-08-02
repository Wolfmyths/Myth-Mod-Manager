
import os

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QUrl

from widgets.contextMenu import ModContextMenu
from widgets.progressWidget import StartFileMover
from widgets.deleteWarningQDialog import DeleteModConfirmation
from widgets.newModQDialog import newModLocation
import errorChecking
from save import Save, OptionsManager
from constant_vars import MOD_ENABLED, TYPE_MODS, TYPE_MODS_OVERRIDE, OPTIONS_GAMEPATH, OPTIONS_DISPATH, MOD_TYPE, MODSIGNORE, MODS_DISABLED_PATH_DEFAULT

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
    
    def getSelectedNameItems(self) -> list[qtw.QTableWidgetItem]:
        return self.selectedItems()[::self.columnCount()]
    
    def getModTypeCount(self, modType: str) -> int | None:
        '''
        Returns the specified modtype count in the table,
        if an invalid parameter is passed then return None

        Possible Parameters:

        + TYPE_MODS
        + TYPE_MODS_OVERRIDE
        '''

        if modType in (TYPE_MODS, TYPE_MODS_OVERRIDE):
            return len(self.findItems(modType, qt.MatchFlag.MatchExactly))
    
    def changeSortState(self, header: int) -> None:
        '''
        Changes the sort state based off the header's index that wants to be sorted
        
        If the header is already the one being sorted, then reverse the order from
        ascending to descending
        '''

        if self.sortState['col'] == header:

            self.sortState['ascending'] = not self.sortState['ascending']

        self.sortState['col'] = header

        self.sort()
    
    def sort(self):
        '''Sorts the table widget based on the sort state, see changeSortState()'''

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
        '''
        Sets one or more mods to be disabled in MOD_CONFIG and in the GUI
        
        If the mod specified is enabled already then continue to the next
        iteration
        '''

        items = self.getSelectedNameItems()

        startFileMover = StartFileMover(0, *[x.text() for x in items])
        startFileMover.exec()

        for item in items:

            row = item.row()

            modName = item.text()

            if self.saveManager.isEnabled(modName):

                self.saveManager[modName][MOD_ENABLED] = 'False'

                self.saveManager.writeData()

                self.getEnabledItem(row).setText('Disabled')

                StartFileMover(0, modName)
    
    def deleteItem(self) -> None:
        '''
        Deletes an row from the GUI,
        and the mod assosiated with that row from the user's PC
        '''

        warning = DeleteModConfirmation(self)
        warning.exec()

        if warning.result():

            items = self.getSelectedNameItems()

            startFileMover = StartFileMover(4, *[x.text() for x in items])
            startFileMover.exec()

            for item in items:

                row = item.row()

                self.removeRow(row)
            
            self.itemChanged.emit(*items)
    
    def setItemEnabled(self) -> None:
        '''Sets one or more mods to be enabled in MOD_CONFIG and in the GUI'''

        items = self.getSelectedNameItems()

        startFileMover = StartFileMover(1, *[x.text() for x in items])
        startFileMover.exec()

        for item in items:

            row = item.row()

            modName = item.text()

            self.saveManager[modName][MOD_ENABLED] = 'True'

            self.getEnabledItem(row).setText('Enabled')

        self.saveManager.writeData()
    
    # This isn't used anywhere, might be removed later
    def isMultipleSelected(self) -> bool:
        return len(self.selectedItems()) > 1
    
    def refreshMods(self, sorting: bool = True) -> None:
        '''Refreshes the mod lists in the manager'''

        if self.rowCount() > 0:
            self.setRowCount(0)

        # Gather mods from directories
        mods = self.getMods()

        # Save mods into .ini
        self.saveManager.addMods((mods[0], TYPE_MODS_OVERRIDE), (mods[1], TYPE_MODS))

        # Just incase disabled folder doesn't exist
        errorChecking.createDisabledModFolder()

        disModFolder = self.optionsManager.getOption(OPTIONS_DISPATH)
        disModFolderContents = os.listdir(disModFolder)

        # Add mods to the table widget
        for mod in (x for x in mods[0] + mods[1]):

            type = self.saveManager.getType(mod)
            isEnabled = mod not in disModFolderContents

            if isEnabled:
                self.saveManager[mod][MOD_ENABLED] = 'True'
            else:
                self.saveManager[mod][MOD_ENABLED] = 'False'

            self.addMod(name=mod, type=type, enabled=isEnabled)
        
        # Save changes
        self.saveManager.writeData()

        # Clear selections from the disabled mod check
        self.clearSelection()

        if sorting:
            self.sort()

    def getMods(self) -> list[list[str]]:
        '''
        Returns a list of two lists that have all of the mods from 
        "\\mods" and "\\assets\\mod_overrides"

        Index 0 is "\\assets\\mod_overrides", index 1 is "\\mods"
        '''

        mod_override: list[str] = []
        mods: list[str] = []

        gamePath = self.optionsManager.getOption(OPTIONS_GAMEPATH, fallback='')

        modsPath = os.path.join(gamePath, 'mods')

        mod_overridePath = os.path.join(gamePath, 'assets', 'mod_overrides')

        disabledModsPath = self.optionsManager.getOption(OPTIONS_DISPATH, fallback=MODS_DISABLED_PATH_DEFAULT)

        # Mods Folder
        if os.path.exists(modsPath):

            for mod in os.listdir(modsPath):

                modPath = os.path.join(modsPath, mod)

                if mod not in MODSIGNORE and errorChecking.getFileType(modPath) == 'dir':
                    
                    mods.append(mod)

        # mod_override Folder
        if os.path.exists(mod_overridePath):

            for mod in os.listdir(mod_overridePath):

                modPath = os.path.join(mod_overridePath, mod)

                if errorChecking.getFileType(modPath) == 'dir':

                    mod_override.append(mod)

        # Disabled Mods Folder
        if os.path.exists(disabledModsPath):
            
            for mod in os.listdir(disabledModsPath):

                if self.saveManager.has_section(mod):
                    
                    if self.saveManager[mod][MOD_TYPE] == TYPE_MODS:

                        mods.append(mod)
                    
                    elif self.saveManager[mod][MOD_TYPE] == TYPE_MODS_OVERRIDE:

                        mod_override.append(mod)

        return [mod_override, mods]
    
    def search(self, input: str) -> None:

        results = self.findItems(f'{input}*', qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly)

        for i in range(0, self.rowCount() + 1):

            self.setRowHidden(i, True) if self.item(i, 0) not in results else self.setRowHidden(i, True)


# EVENTS
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
        All cases except where files can be moved should end in `event.ignore()` then `return`
        to prevent the file from automatically being put into the recycling bin

        The only exception to this is when the file being dropped is a regular folder
        '''

        if event.mimeData().hasUrls():

            urls = event.mimeData().urls()

            dirs: list[QUrl] = []
            zips: list[QUrl] = []

            for mod in urls:

                fileType = errorChecking.getFileType(mod.toLocalFile())

                if fileType == 'dir':
                    dirs.append(mod)

                elif fileType == 'zip':
                    zips.append(mod)
            
            notice = newModLocation(*list(dirs + zips))
            notice.exec()

            dict_ = notice.typeDict

            if not len(dict_):
                event.ignore()
                return

            if dirs:

                dirTuple: list[tuple[QUrl, str]] = []

                for dir in dirs:
                    dirTuple.append((dir, dict_.get( dir.fileName() )))

                startFileMover = StartFileMover(2, *dirTuple)
                startFileMover.exec()

            if zips:

                zipsTuple: list[tuple[QUrl, str]] = []

                for zip in zips:
                    zipsTuple.append((zip, dict_.get( zip.fileName() )))

                print(zipsTuple)
                startFileMover = StartFileMover(3, *zipsTuple)
                startFileMover.exec()
            
            self.refreshMods()

            event.ignore()

        else:
            event.ignore()