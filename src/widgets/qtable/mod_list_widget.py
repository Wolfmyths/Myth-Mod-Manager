import os
import logging
from typing import List

import PySide6.QtGui as qtg
import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QCoreApplication as qapp, Slot, Signal

from src.widgets.qmenu.manager_menu import ManagerMenu
from src.widgets.qdialog.progress_widget import ProgressWidget
from src.widgets.qdialog.confirmation import Confirmation
from src.widgets.qdialog.new_mod_location import NewModLocation
from src.widgets.qdialog.notice import Notice
from src.widgets.qwidget.tag_viewer import TagViewer

from src.objects.move_to_disabled_dir import MoveToDisabledDir
from src.objects.move_to_enabled_dir import MoveToEnabledModDir
from src.objects.change_mod_type import ChangeModType
from src.objects.delete_mod import DeleteMod
from src.objects.unzip_mod import UnZipMod

from src.helpers.helper_pathing import Pathing
import src.helpers.helper as helper
from src.helpers.options_manager import OptionsManager
from src.helpers.save_manager import Save
from src.constant_vars import MODSIGNORE, ModType, UI_GRAPHICS_PATH, MODWORKSHOP_LOGO_B, MODWORKSHOP_LOGO_W, LIGHT, ModRole
from src.api.api import findModworkshopAssetID, findModVersion
from src.api.check_mod_update import CheckModUpdate

class ModListWidget(qtw.QTableWidget):
    modHidden = Signal()

    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.setSelectionMode(qtw.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setSelectionBehavior(qtw.QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(qtw.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAcceptDrops(True)

        self.setColumnCount(4)

        self.setColumnWidth(0, 400)
        self.setColumnWidth(1, 130)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)

        horizontalHeader: qtw.QHeaderView = self.horizontalHeader()

        horizontalHeader.sectionClicked.connect(self.sort)
        horizontalHeader.setHighlightSections(False)

        horizontalHeader.setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.Stretch)
        horizontalHeader.setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.ResizeToContents)
        horizontalHeader.setSectionResizeMode(2, qtw.QHeaderView.ResizeMode.ResizeToContents)
        horizontalHeader.setSectionResizeMode(3, qtw.QHeaderView.ResizeMode.Interactive)

        self.sortState: dict[str:int | qt.SortOrder] = {
            'col' : 0,
            'ascending': qt.SortOrder.AscendingOrder
        }

        self.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.verticalHeader().hide()

        self.contextMenu = ManagerMenu(self)
        self.tagViewer = None

        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.setHorizontalHeaderLabels((
            qapp.translate("ModListWidget", 'Name'),
            qapp.translate("ModListWidget", 'Type'),
            qapp.translate("ModListWidget", 'Enabled'),
            qapp.translate("ModListWidget", 'Version'))
        )

        # Update Enabled Item Tags
        enabled_text: str = self.horizontalHeaderItem(2).text()
        disabled_text: str = qapp.translate("ModListWidget", 'Disabled')

        for i, item in enumerate(self.getEnabledItems()):
            if Save.getEnabled(self.getNameItem(i).text()):
                item.setText(enabled_text)
            else:
                item.setText(disabled_text)

    def getEnabledItem(self, row: int) -> qtw.QTableWidgetItem:
        return self.item(row, 2)
    
    def getEnabledItems(self) -> list[qtw.QTableWidgetItem]:
        return [
            self.getEnabledItem(x) for x in range(self.rowCount())
        ]
    
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

        if helper.isTypeMod(modType):
            return len(self.findItems(modType.value, qt.MatchFlag.MatchExactly))
    
    @Slot(int)
    @Slot(int, bool)
    def sort(self, header: int, changeAscending = True) -> None:
        '''
        Sorts the table widget based on the header selected.

        If `header` is equal to `self.sortState['col']`
        reverse the order unless specified with `changeAscending`.
        '''

        if header == self.sortState['col'] and changeAscending:

            inverseDict: dict[qt.SortOrder, qt.SortOrder] = {
                qt.SortOrder.AscendingOrder : qt.SortOrder.DescendingOrder, 
                qt.SortOrder.DescendingOrder : qt.SortOrder.AscendingOrder
            }

            currentSort: qt.SortOrder = self.sortState['ascending']

            self.sortState['ascending'] = inverseDict[currentSort]

        self.sortState['col'] = header
        
        logging.debug('Sorting items by col: %s, ascending: %s', self.sortState.get('col'), self.sortState.get('ascending'))

        self.sortItems(self.sortState['col'], self.sortState['ascending'])
    
    def addMod(self, **kwargs: str | ModType | bool | list[str]) -> None:
        '''
        Adds a new mod to the table (Not in the save manager)

        Accepted kwargs:

        + name : str
        + type : ModType
        + enabled : bool
        + version: str
        + tags: list[str]

        If there is any other kwarg, then it will return
        '''

        self.insertRow(self.rowCount())

        for key, value in kwargs.items():

            match key:

                case 'name':
                    item = qtw.QTableWidgetItem(value)
                    tags: str | ModType | bool | List[str] | None = kwargs.get('tags')
                    if tags is None:
                        tags = []
                    item.setData(ModRole.tags, tuple(tags))

                    if Save.getModworkshopAssetID(value):

                        color = MODWORKSHOP_LOGO_B if OptionsManager.getTheme() == LIGHT else MODWORKSHOP_LOGO_W

                        item.setIcon(qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, color)))

                    self.setItem(self.rowCount() - 1, 0, item)


                case 'type':
                    self.setItem(self.rowCount() - 1, 1, qtw.QTableWidgetItem(value.value))

                case 'enabled': # The key to this value should be a boolean

                    value: str = qapp.translate('ModListWidget', 'Enabled') if value else qapp.translate('ModListWidget', 'Disabled')
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

        items: List[qtw.QTableWidgetItem] = self.getSelectedNameItems()

        disabledModDir: str = OptionsManager.getDispath()

        startFileMover = ProgressWidget(MoveToDisabledDir(*[x.text() for x in items]))
        startFileMover.exec()

        for item in items:

            row: int = item.row()

            modName: str = item.text()

            if os.path.isdir(os.path.join(disabledModDir, modName)):

                Save.setEnabled(modName, False)

                self.getEnabledItem(row).setText(qapp.translate("ModListWidget", 'Disabled'))

            else:
                logging.info('%s is already disabled in the save file', modName)
        
        Save.saveJSON()

    def deleteItem(self) -> None:
        '''
        Deletes an row from the GUI,
        and the mod assosiated with that row from the user's PC
        '''

        warning = Confirmation(
            title='Deletion Confirmation', 
            body='Are you sure you want to delete these mod(s) from your computer?\n(The mods will be placed in the recycle bin)'
        )
        warning.exec()

        if warning.result():

            items: List[qtw.QTableWidgetItem] = self.getSelectedNameItems()

            startFileMover = ProgressWidget(DeleteMod(*[x.text() for x in items]))
            startFileMover.exec()

            for item in items:

                row: int = item.row()

                self.removeRow(row)
            
            self.itemChanged.emit(*items)

            Save.saveJSON()
    
    def setItemEnabled(self) -> None:
        '''Sets one or more mods to be enabled in MOD_CONFIG and in the GUI'''

        items: List[qtw.QTableWidgetItem] = self.getSelectedNameItems()

        startFileMover = ProgressWidget(MoveToEnabledModDir(*[x.text() for x in items]))
        startFileMover.exec()

        for item in items:

            row: int = item.row()

            modName: str = item.text()
            modType = ModType(self.getTypeItem(row).text())

            Pathing.mod(modType, modName)

            if os.path.isdir(Pathing.mod(modType, modName)):
                Save.setEnabled(modName, True)

                self.getEnabledItem(row).setText(qapp.translate("ModListWidget", 'Enabled'))
        
        Save.saveJSON()

    # This isn't used anywhere, might be removed later
    def isMultipleSelected(self) -> bool:
        return len(self.selectedItems()) > 1
    
    @Slot()
    @Slot(bool)
    def refreshMods(self, sorting: bool = True) -> None:
        '''Refreshes the mod lists in the manager'''

        if self.rowCount() > 0:
            self.setRowCount(0)

        # Gather mods from directories
        mods_override, mods, maps = self.getMods()

        # Save mods into .ini
        Save.addMods((mods_override, ModType.mods_override), (mods, ModType.mods), (maps, ModType.maps))

        disModFolder: str = OptionsManager.getDispath()

        # Add mods to the table widget
        for mod in (x for x in mods_override + mods + maps):
            
            # Checking if the mod is ignored
            if Save.getIgnored(mod):
                continue

            type: ModType | None = Save.getType(mod)
            isEnabled: bool = not os.path.isdir(os.path.join(disModFolder, mod))
            modPath: List[str] | str = Pathing.mod(type, mod) if isEnabled else os.path.join(disModFolder, mod)
            version = str(findModVersion(modPath))
            tags: List[str] = Save.getTags(mod)

            assetID: str = Save.getModworkshopAssetID(mod)

            # Empty string
            if not assetID:
                assetID = findModworkshopAssetID(modPath)

            Save.setEnabled(mod, isEnabled)
            
            Save.setModWorkshopAssetID(mod, assetID)
            
            logging.debug('Adding mod to table, %s|%s|%s|%s|%s|%s', mod, type, isEnabled, version, assetID, tags)

            self.addMod(name=mod, type=type, enabled=isEnabled, version=version, tags=tags)
        
        Save.saveJSON()

        # Clear selections from the disabled mod check
        self.clearSelection()

        if sorting:
            self.sort(self.sortState['col'], False)

    def getMods(self) -> list[list[str]]:
        '''
        Returns a list of two lists that have all of the mods from 
        "\\mods", "\\Maps" and "\\assets\\mod_overrides"

        Returning Indexes:
        + 0: mod_overrides
        + 1: mods
        + 2: Maps
        '''

        # Valid mods
        mod_override: list[str] = []
        mods: list[str] = []
        maps: list[str] = []

        # Mod Folder Paths
        modsPath: str = Pathing.mods()
        mod_overridePath: str = Pathing.mod_overrides()
        maps_path: str = Pathing.maps()
        disabledModsPath: str = OptionsManager.getDispath()

        # Mod Folder Contents
        modsFolder: List[str] = os.listdir(modsPath)
        mod_overrideFolder: List[str] = os.listdir(mod_overridePath)
        mapsFolder: List[str] = os.listdir(maps_path)
        disabledModsFolder: List[str] = os.listdir(disabledModsPath)

        # Mods Folder
        if os.path.exists(modsPath):

            for mod in modsFolder:

                modPath = os.path.join(modsPath, mod)

                if mod not in MODSIGNORE and helper.getFileType(modPath) == 'dir':
                    
                    mods.append(mod)
        else:
            logging.error('The mods path does not exist:\n%s\nSkipping...', modsPath)

        # mod_override Folder
        if os.path.exists(mod_overridePath):

            for mod in mod_overrideFolder:

                modPath = os.path.join(mod_overridePath, mod)

                if helper.getFileType(modPath) == 'dir':

                    mod_override.append(mod)
        else:
            logging.error('The mod_overrides path does not exist:\n%s\nSkipping...', mod_overridePath)

        # maps Folder
        if os.path.exists(maps_path):

            for mod in mapsFolder:

                modPath: str = os.path.join(maps_path, mod)

                if helper.getFileType(modPath) == 'dir':

                    maps.append(mod)
        else:
            logging.error('The modded maps path does not exist:\n%s\nSkipping...', maps_path)

        # Disabled Mods Folder
        if os.path.exists(disabledModsPath):
            
            for mod in disabledModsFolder:

                if Save.hasMod(mod):

                    modType: ModType | None = Save.getType(mod)
                    
                    if modType == ModType.mods:

                        mods.append(mod)
                    
                    elif modType == ModType.mods_override:

                        mod_override.append(mod)
                    
                    elif modType == ModType.maps:

                        maps.append(mod)
                else:
                    logging.error('%s needs to be installed first before becoming disabled', mod)

        return mod_override, mods, maps
    
    def visitModPage(self) -> None:

        if not len(self.getSelectedNameItems()) <= 0:
            selectedItem: qtw.QTableWidgetItem = self.getSelectedNameItems()[0]

            assetID: str = Save.getModworkshopAssetID(selectedItem.text())

            helper.openWebPage(f'https://modworkshop.net/mod/{assetID}')
    
    def CheckModUpdate(self) -> None:
        notice_title: str = qapp.translate("ModListWidget", 'Mod Update Check Results')
        @Slot(str)
        def updateDetected(newVersion: str) -> None:
            Notice(
                qapp.translate("ModListWidget", 'A new version has been found for') + f' {modName}!' + '\n' + qapp.translate("ModListWidget", 'Local') + f': {modVersion}\nModworkshop: {newVersion}',
                notice_title
            ).exec()
        @Slot()
        def uptoDate() -> None:
            Notice(modName + ' ' + qapp.translate("ModListWidget", 'is up to date'), notice_title).exec()

        item: qtw.QTableWidgetItem = self.getSelectedNameItems()[0]
        modName: str = self.getNameItem(self.row(item)).text()
        modVersion: str = self.getVersionItem(self.row(item)).text()
        assetID: str = Save.getModworkshopAssetID(modName)

        if not assetID:
            logging.warning('ModListWidget.CheckModUpdate(), %s is missing an assetID', modName)
            return

        self.api = CheckModUpdate(assetID, modVersion)
        self.api.upToDate.connect(uptoDate)
        self.api.updateDetected.connect(updateDetected)

    def openModDir(self) -> None:
        if not len(self.getSelectedNameItems()) <= 0:
            selectedItem: qtw.QTableWidgetItem = self.getSelectedNameItems()[0]

            modName: str = self.getNameItem(self.row(selectedItem)).text()
            modType: str = self.getTypeItem(self.row(selectedItem)).text()

            path: str | list[str]
            if not Save.getEnabled(modName):
                path = os.path.join(OptionsManager.getDispath(), modName)
            else:
                path = Pathing.mod(ModType(modType), modName)

            if os.path.isdir(path):
                helper.startFile(path)

    def hideMod(self) -> None:
        items: List[qtw.QTableWidgetItem] = self.getSelectedNameItems()
        for item in items:
            modName: str = item.text()
            Save.setIgnored(modName, True)
            self.removeRow(item.row())
        
        Save.saveJSON()

        self.modHidden.emit()
        self.itemChanged.emit(items[0])

    def viewTags(self) -> None:
        self.tagViewer = TagViewer(self)
        self.tagViewer.tagChanged.connect(lambda x, y: self.updateTags(x, y))
        self.tagViewer.show()
    
    @Slot(str, tuple)
    def updateTags(self, mod: str, tags: tuple[str]) -> None:
        items: List[qtw.QTableWidgetItem] = self.findItems(mod, qt.MatchFlag.MatchFixedString)
        if items:
            item: qtw.QTableWidgetItem = items[0]
            item.setData(ModRole.tags, sorted(tags))

    @Slot(str)
    def search(self, input: str) -> None:
        searchedTags = None

        if input.startswith('tag:') and len(input) > 4:
            splitStr: List[str] = input.split(' ')
            input = ' '.join(splitStr[1:])
            searchedTags: List[str] = splitStr[0][4:].split(',')

        results: List[qtw.QTableWidgetItem] = self.findItems(
            f'{input}*',
            qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchExactly
        )

        for i in range(0, self.rowCount() + 1):

            item: qtw.QTableWidgetItem | None = self.item(i, 0)
            if item is not None:
                modTags: tuple[str] | None = item.data(ModRole.tags)

            if searchedTags is not None and modTags is not None:
                for tag in searchedTags:
                    if tag in modTags and item in results:
                        self.setRowHidden(i, False)
                    else:
                        self.setRowHidden(i, True)
            else:
                if item in results and searchedTags is None:
                    self.setRowHidden(i, False)
                else:
                    self.setRowHidden(i, True)
    
    @Slot(str)
    def swapIcons(self, mode: str) -> None:

        newIcon = MODWORKSHOP_LOGO_W if mode == LIGHT else MODWORKSHOP_LOGO_B

        reverseDict: dict[str, str] = {
            MODWORKSHOP_LOGO_B : MODWORKSHOP_LOGO_W,
            MODWORKSHOP_LOGO_W : MODWORKSHOP_LOGO_B
        }

        for i in range(0, self.rowCount() - 1):
            item: qtw.QTableWidgetItem = self.getNameItem(i)

            if not item.icon().isNull():
                item.setIcon(qtg.QIcon(os.path.join(UI_GRAPHICS_PATH, reverseDict[newIcon])))

    def installMods(self, *urls: str) -> None:

        dirs: list[str] = [x for x in urls if helper.getFileType(x) == 'dir']
        zips: list[str] = [x for x in urls if helper.getFileType(x) == 'zip']

        # Gather where the user wants each mod to go
        notice = NewModLocation(*[x for x in list(dirs + zips)])
        notice.exec()

        if not notice.result():
            return

        # Dictionary holding the destination for each mod
        dict_: dict = notice.typeDict

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
        self.refreshMods()

# EVENT OVERRIDES
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:

        if event.button() == qt.MouseButton.RightButton:
            
            # Will return None if there are no mods causing a traceback
            tableWidgetItem: qtw.QTableWidgetItem | None = self.itemAt(event.pos())

            if tableWidgetItem is not None:

                if len(self.getSelectedNameItems()) <= 1:
                    self.selectRow(tableWidgetItem.row())
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
