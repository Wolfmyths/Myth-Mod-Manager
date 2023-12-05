import os
import logging

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.widgets.QMenu.managerQMenu import ManagerMenu
from src.widgets.progressWidget import ProgressWidget
from src.widgets.QDialog.deleteWarningQDialog import DeleteModConfirmation
from src.widgets.QDialog.newModQDialog import newModLocation

from src.threaded.moveToDisabledDir import MoveToDisabledDir
from src.threaded.moveToEnabledDir import MoveToEnabledModDir
from src.threaded.changeModType import ChangeModType
from src.threaded.deleteMod import DeleteMod
from src.threaded.unZipMod import UnZipMod

from src.getPath import Pathing
import src.errorChecking as errorChecking
from src.save import Save, OptionsManager
from src.constant_vars import MODSIGNORE, ModType, UI_GRAPHICS_PATH, MODWORKSHOP_LOGO_B, MODWORKSHOP_LOGO_W, LIGHT, MOD_CONFIG, OPTIONS_CONFIG
from src.api.api import findModworkshopAssetID, findModVersion

class ModListWidget(qtw.QTableWidget):

    def __init__(self, savePath: str = MOD_CONFIG, optionsPath: str = OPTIONS_CONFIG) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.setObjectName('modlistwidget')

        self.saveManager = Save(savePath)
        self.optionsManager = OptionsManager(optionsPath)

        self.p = Pathing(optionsPath)

        self.setSelectionMode(qtw.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(qtw.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAcceptDrops(True)

        self.setColumnCount(4)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 125)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)

        self.setHorizontalHeaderLabels(('Name', 'Type', 'Enabled', 'Version'))

        horizontalHeader = self.horizontalHeader()

        horizontalHeader.sectionClicked.connect(lambda x: self.sort(x))
        horizontalHeader.setHighlightSections(False)

        horizontalHeader.setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.Stretch)
        horizontalHeader.setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSectionResizeMode(2, qtw.QHeaderView.ResizeMode.Interactive)
        horizontalHeader.setSectionResizeMode(3, qtw.QHeaderView.ResizeMode.Interactive)

        self.sortState = {'col' : 0, 'ascending': qt.SortOrder.AscendingOrder}

        self.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalHeader().hide()

        self.contextMenu = ManagerMenu(self)
    
    def getEnabledItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 2)
    
    def getNameItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 0)
    
    def getTypeItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 1)
    
    def getVersionItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 3)
    
    def getSelectedNameItems(self) -> list[qtw.QTableWidgetItem]:
        return self.selectedItems()[::self.columnCount()]
    
    def getModTypeCount(self, modType: ModType) -> int | None:
        '''
        Returns the specified modtype count in the table,
        if an invalid parameter is passed then return None
        '''

        if errorChecking.isTypeMod(modType):
            return len(self.findItems(modType.value, qt.MatchFlag.MatchExactly))
    
    def sort(self, header: int, changeAscending = True) -> None:
        '''
        Sorts the table widget based on the header selected.

        If `header` is equal to `self.sortState['col']`
        reverse the order unless specified with `changeAscending`.
        '''

        if header == self.sortState['col'] and changeAscending:

            inverseDict = {qt.SortOrder.AscendingOrder : qt.SortOrder.DescendingOrder, 
                           qt.SortOrder.DescendingOrder : qt.SortOrder.AscendingOrder}

            currentSort = self.sortState['ascending']

            self.sortState['ascending'] = inverseDict[currentSort]

        self.sortState['col'] = header
        
        logging.debug('Sorting items by col: %s, ascending: %s', self.sortState.get('col'), self.sortState.get('ascending'))

        self.sortItems(self.sortState['col'], self.sortState['ascending'])
    
    def addMod(self, **kwargs: str | ModType | bool) -> None:
        '''
        Adds a new mod to the table (Not in the save manager)

        Accepted kwargs:

        + name : str
        + type : ModType
        + enabled : bool
        + version: str

        If there is any other kwarg, then it will return
        '''

        self.insertRow(self.rowCount())

        for key, value in kwargs.items():

            match key:

                case 'name':
                    item = qtw.QTableWidgetItem(value)

                    if self.saveManager.getModworkshopAssetID(value):

                        color = MODWORKSHOP_LOGO_B if self.optionsManager.getTheme() == LIGHT else MODWORKSHOP_LOGO_W

                        item.setIcon(qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, color)))

                    self.setItem(self.rowCount() - 1, 0, item)


                case 'type':
                    self.setItem(self.rowCount() - 1, 1, qtw.QTableWidgetItem(value.value))

                case 'enabled': # The key to this value should be a boolean

                    value = 'Enabled' if value else 'Disabled'
                    self.setItem(self.rowCount() - 1, 2, qtw.QTableWidgetItem(value))
                
                case 'version':

                    if value == 'None':
                        value = '1.0.0'

                    self.setItem(self.rowCount() - 1, 3, qtw.QTableWidgetItem(value))

                case _:
                    continue
    
    def setItemDisabled(self) -> None:
        '''
        Sets one or more mods to be disabled in MOD_CONFIG and in the GUI
        
        If the mod specified is enabled already then continue to the next
        iteration
        '''

        items = self.getSelectedNameItems()

        startFileMover = ProgressWidget(MoveToDisabledDir(*[x.text() for x in items]))
        startFileMover.exec()

        for item in items:

            row = item.row()

            modName = item.text()

            if self.saveManager.getEnabled(modName):

                self.saveManager.setEnabled(modName, False)
                self.getEnabledItem(row).setText('Disabled')

            else:
                logging.info('%s is already disabled in the save file', modName)
        
        self.saveManager.writeData()

    def deleteItem(self) -> None:
        '''
        Deletes an row from the GUI,
        and the mod assosiated with that row from the user's PC
        '''

        warning = DeleteModConfirmation(self)
        warning.exec()

        if warning.result():

            items = self.getSelectedNameItems()

            startFileMover = ProgressWidget(DeleteMod(*[x.text() for x in items]))
            startFileMover.exec()

            for item in items:

                row = item.row()

                self.removeRow(row)
            
            self.itemChanged.emit(*items)

            self.saveManager.writeData()
    
    def setItemEnabled(self) -> None:
        '''Sets one or more mods to be enabled in MOD_CONFIG and in the GUI'''

        items = self.getSelectedNameItems()

        startFileMover = ProgressWidget(MoveToEnabledModDir(*[x.text() for x in items]))
        startFileMover.exec()

        for item in items:

            row = item.row()

            modName = item.text()

            self.saveManager.setEnabled(modName, True)

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
        self.saveManager.addMods((mods[0], ModType.mods_override), (mods[1], ModType.mods), (mods[2], ModType.maps))

        disModFolder = self.optionsManager.getDispath()
        disModFolderContents = os.listdir(disModFolder)

        # Add mods to the table widget
        for mod in (x for x in mods[0] + mods[1] + mods[2]):
            
            # Checking if the mod is ignored
            if self.saveManager.getIgnored(mod):
                continue

            type = self.saveManager.getType(mod)
            modPath = self.p.mod(type, mod)
            version = str(findModVersion(modPath))
            isEnabled = mod not in disModFolderContents

            assetID = self.saveManager.getModworkshopAssetID(mod)

            if not assetID:
                assetID = findModworkshopAssetID(modPath)

            self.saveManager.setEnabled(mod, isEnabled)
            
            self.saveManager.setModWorkshopAssetID(mod, assetID)
            
            logging.debug('Adding mod to table, %s|%s|%s|%s|%s', mod, type, isEnabled, version, assetID)

            self.addMod(name=mod, type=type, enabled=isEnabled, version=version)
        
        self.saveManager.writeData()

        # Clear selections from the disabled mod check
        self.clearSelection()

        if sorting:
            self.sort(self.sortState['col'], False)

    def getMods(self) -> list[list[str]]:
        '''
        Returns a list of two lists that have all of the mods from 
        "\\mods" and "\\assets\\mod_overrides"

        Index 0 is "\\assets\\mod_overrides", index 1 is "\\mods"
        '''

        mod_override: list[str] = []
        mods: list[str] = []
        maps: list[str] = []

        modsPath = self.p.mods()

        mod_overridePath = self.p.mod_overrides()

        maps_path = self.p.maps()

        disabledModsPath = self.optionsManager.getDispath()

        # Mods Folder
        if os.path.exists(modsPath):

            for mod in os.listdir(modsPath):

                modPath = os.path.join(modsPath, mod)

                if mod not in MODSIGNORE and errorChecking.getFileType(modPath) == 'dir':
                    
                    mods.append(mod)
        else:
            logging.error('The mods path does not exist:\n%s\nSkipping...', modsPath)

        # mod_override Folder
        if os.path.exists(mod_overridePath):

            for mod in os.listdir(mod_overridePath):

                modPath = os.path.join(mod_overridePath, mod)

                if errorChecking.getFileType(modPath) == 'dir':

                    mod_override.append(mod)
        else:
            logging.error('The mod_overrides path does not exist:\n%s\nSkipping...', mod_overridePath)

        # maps Folder
        if os.path.exists(maps_path):

            for mod in os.listdir(maps_path):

                modPath = os.path.join(maps_path, mod)

                if errorChecking.getFileType(modPath) == 'dir':

                    maps.append(mod)
        else:
            logging.error('The modded maps path does not exist:\n%s\nSkipping...', maps_path)

        # Disabled Mods Folder
        if os.path.exists(disabledModsPath):
            
            for mod in os.listdir(disabledModsPath):

                if self.saveManager.has_section(mod):

                    modType = self.saveManager.getType(mod)
                    
                    if modType == ModType.mods:

                        mods.append(mod)
                    
                    elif modType == ModType.mods_override:

                        mod_override.append(mod)
                    
                    elif modType == ModType.maps:

                        maps.append(mod)
                else:
                    logging.error('%s needs to be installed first before becoming disabled', mod)

        return [mod_override, mods, maps]
    
    def visitModPage(self) -> None:

        if not len(self.getSelectedNameItems()) <= 0:
            selectedItem = self.getSelectedNameItems()[0]

            assetID = self.saveManager.getModworkshopAssetID(selectedItem.text())

            errorChecking.openWebPage(f'https://modworkshop.net/mod/{assetID}')
    
    def openModDir(self) -> None:
        if not len(self.getSelectedNameItems()) <= 0:
            selectedItem = self.getSelectedNameItems()[0]

            modName = self.getNameItem(self.row(selectedItem)).text()
            modType = self.getTypeItem(self.row(selectedItem)).text()

            path = self.p.mod(ModType(modType), modName)

            if os.path.exists(path):
                os.startfile(path)

    def hideMod(self) -> None:
        items = self.getSelectedNameItems()
        for item in items:
            modName = item.text()
            self.saveManager.setIgnored(modName, True)
            self.removeRow(item.row())
        
        self.saveManager.writeData()

        self.itemChanged.emit(items[0])
    
    def search(self, input: str) -> None:

        results = self.findItems(f'{input}*', qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly)

        for i in range(0, self.rowCount() + 1):

            item = self.item(i, 0)

            if item not in results:
                self.setRowHidden(i, True)
            else:
                self.setRowHidden(i, False)
    
    def swapIcons(self) -> None:

        newIcon = MODWORKSHOP_LOGO_W if self.optionsManager.getTheme() == LIGHT else MODWORKSHOP_LOGO_B

        reverseDict = {MODWORKSHOP_LOGO_B : MODWORKSHOP_LOGO_W, MODWORKSHOP_LOGO_W : MODWORKSHOP_LOGO_B}

        for i in range(0, self.rowCount() - 1):
            item = self.getNameItem(i)

            if not item.icon().isNull():
                item.setIcon(qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, reverseDict[newIcon])))

    def installMods(self, *urls: str) -> None:

        dirs: list[str] = [x for x in urls if errorChecking.getFileType(x) == 'dir']
        zips: list[str] = [x for x in urls if errorChecking.getFileType(x) == 'zip']

        # Gather where the user wants each mod to go
        notice = newModLocation(*[x for x in list(dirs + zips)])
        notice.exec()

        if not notice.result():
            return

        # Dictionary holding the destination for each mod
        dict_ = notice.typeDict

        # Combine the mod location and URL into a Tuple
        if dirs:

            dirTuple: list[tuple[str, ModType]] = []

            for dir in dirs:
                dirTuple.append((dir, dict_[os.path.basename(dir)]))

            startFileMover = ProgressWidget(ChangeModType(*dirTuple))
            startFileMover.exec()

        if zips:

            zipsTuple: list[tuple[str, ModType]] = []

            for zip in zips:
                zipsTuple.append((zip, dict_[os.path.basename(zip)]))

            startFileMover = ProgressWidget(UnZipMod(*zipsTuple))
            startFileMover.exec()
    
        self.itemChanged.emit(qtw.QTableWidgetItem())

# EVENT OVERRIDES
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:

        if event.button() == qt.MouseButton.RightButton:
            
            if len(self.getSelectedNameItems()) <= 1:
                self.selectRow(self.itemAt(event.pos()).row())
            self.contextMenu.exec(qtg.QCursor.pos())

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

            logging.info('Drop event with URLs detected')

            self.installMods(*[x.toLocalFile() for x in event.mimeData().urls()])

        event.ignore()
