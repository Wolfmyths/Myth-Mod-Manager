import logging

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
from PySide6.QtCore import Qt as qt, Signal, QCoreApplication as qapp, Slot
from typing_extensions import override

from src.widgets.qmenu.profile_menu import ProfileMenu
from src.widgets.qdialog.insert_string import InsertString
from src.widgets.qdialog.notice import Notice
from src.widgets.qdialog.select_mod import SelectMod
from src.widgets.qdialog.select_profile import SelectProfile

import src.helpers.helper as helper
from src.helpers.profile_manager import ProfileManager
from src.constant_vars import DATA_PROFILE, DATA_MOD, ProfileRole

class ProfileList(qtw.QTreeWidget):

    applyProfile = Signal(tuple)

    profileRightclicked = Signal()

    modRightclicked = Signal()

    noneRightclicked = Signal()

    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)

        logging.getLogger(__name__)

        self.setHorizontalScrollBarPolicy(qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setColumnCount(2)

        self.header().setSectionResizeMode(0, qtw.QHeaderView.ResizeMode.Stretch)
        self.header().setSectionResizeMode(1, qtw.QHeaderView.ResizeMode.Interactive)

        self.menu = ProfileMenu(self)
        self.menu.profileApply.triggered.connect(self.applyProfileEvent)
        self.menu.profileAdd.triggered.connect(self.menuAddProfile)
        self.menu.profileRemove.triggered.connect(self.deleteProfile)
        self.menu.profileEdit.triggered.connect(self.editProfileMenu)
        self.menu.profileCopy.triggered.connect(self.copyProfile)
        self.menu.modAdd.triggered.connect(self.modAddMenu)
        self.menu.modRemove.triggered.connect(self.removeMods)
        self.menu.copyModsTo.triggered.connect(self.copyModsToProfileMenu)

        self.profileRightclicked.connect(self.menu.profileRightClicked)
        self.modRightclicked.connect(self.menu.modRightClicked)
        self.noneRightclicked.connect(self.menu.noneRightClicked)

        self.updateView()
        self.applyStaticText()

    def applyStaticText(self) -> None:
        self.setHeaderLabels(
            (
                qapp.translate('ProfileList', 'Profile'),
                qapp.translate('ProfileList', 'Mod Count')
            )
        )

    def __getProfiles(self) -> list[str]:
        return [x.text(0) for x in self.findItems('*', qt.MatchFlag.MatchWildcard | qt.MatchFlag.MatchWrap | qt.MatchFlag.MatchRecursive) if self.isProfile(x)]

    def __findProfile(self, profile: str) -> qtw.QTreeWidgetItem:
        return self.findItems(profile, qt.MatchFlag.MatchExactly)[0]

    def __getParentOfChild(self, child: qtw.QTreeWidgetItem) -> qtw.QTreeWidgetItem:
        return self.__findProfile(child.data(0, ProfileRole.parent))

    def __getMods(self, profile: qtw.QTreeWidgetItem) -> list[qtw.QTreeWidgetItem]:
        '''Returns a list of mod names given the profile'''
        mods: list[qtw.QTreeWidgetItem] = []

        for i in range(0, profile.childCount() + 1):

            child: qtw.QTreeWidgetItem = profile.child(i)

            if child:
                mods.append(child)

        return mods

    def __selectedItem(self) -> qtw.QTreeWidgetItem | None:
        '''Returns the first object selected in `selectedItems()`'''

        try:

            return self.selectedItems()[0]

        except IndexError:

            logging.warning('IndexError in ProfileList.__selectedItem()')

            return None
    
    @Slot()
    def applyProfileEvent(self) -> None:

        selectedItem: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if selectedItem is not None:

            if self.isProfile(selectedItem):

                logging.info('Applying mods from %s', selectedItem.text(0))

                self.applyProfile.emit(tuple(ProfileManager.getMods(selectedItem.text(0))))
            
            else:

                profile: str = self.__getParentOfChild(selectedItem).text(0)

                logging.info('Applying mods from %s', profile)

                self.applyProfile.emit(tuple(ProfileManager.getMods(profile)))
    
    def checkInstalled(self) -> None:
        '''
        Gives each mod in the tree widget a bool
        depending if it's installed or not.
        '''

        for profile in ProfileManager.get_profile_names():

            profileWidget: qtw.QTreeWidgetItem = self.__findProfile(profile)

            modsWidget: list[qtw.QTreeWidgetItem] | None = self.__getMods(profileWidget)

            if not modsWidget:
                continue

            for mod in modsWidget:

                if helper.isInstalled(mod.text(0)):
                    mod.setData(0, ProfileRole.installed, True)
                else:
                    mod.setData(0, ProfileRole.installed, False)

    def updateView(self) -> None:
        '''Refreshes the whole widget'''
        
        self.clear()

        profile: str
        for profile in ProfileManager.get_profile_names():

            modList: list[str] = ProfileManager.getMods(profile)

            self.addProfile(profile, initalize=True)

            profileWidget: qtw.QTreeWidgetItem = self.__findProfile(profile)

            profileWidget.setSelected(True)

            # Save is set to false since we know whatever's in the mod list already exists
            self.addMods(*modList, save=False)

            profileWidget.setSelected(False)
            
            self.addTopLevelItem(profileWidget)
        
        self.checkInstalled()
    
    @Slot()
    def modAddMenu(self) -> None:
        qDialog = SelectMod()

        qDialog.exec()

        if qDialog.result():

            self.addMods(*qDialog.mods)


    def addMods(self, *mods: str, save: bool = True) -> None:

        selectedItem: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if selectedItem is None:
            return

        # If this function was triggered by selecting a mod, find the profile
        profile: qtw.QTreeWidgetItem | None
        if not self.isProfile(selectedItem):
            profile = self.__getParentOfChild(selectedItem)
        else:
            profile = selectedItem
        
        logging.info('Adding mods: %s into profile: %s', ' ,'.join(mods), profile.text(0))

        profileModsItems: list[qtw.QTreeWidgetItem] | None = self.__getMods(profile)
        profileMods: list[str] = []

        if profileModsItems:
            profileMods = [x.text(0) for x in profileModsItems]

        for mod in mods:
            
            # Preventing duplicate mods from being added to the GUI
            if profileMods and mod in profileMods:
                logging.warning('%s is a duplicate mod in %s, not adding.', mod, profile.text(0))
                continue

            child = qtw.QTreeWidgetItem([mod])
            child.setData(*DATA_MOD)
            child.setData(0, ProfileRole.parent, profile.text(0))
            child.setData(0, ProfileRole.installed, True)

            profile.addChild(child)

            profile.setText(1, str(int(profile.text(1)) + 1))
        
        if save:
            ProfileManager.addMod(profile.text(0), *mods)

            if not profile.isExpanded():
                profile.setExpanded(True)
    
    @Slot()
    def removeMods(self) -> None:

        mod: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if mod is None:
            return

        profile: qtw.QTreeWidgetItem = self.__getParentOfChild(mod)

        logging.info('Removing mod %s from profile %s', mod.text(0), profile.text(0))

        ProfileManager.removeMod(profile.text(0), mod.text(0))

        profile.takeChild(profile.indexOfChild(mod))

        profile.setText(1, str(int(profile.text(1)) - 1))
    
    @Slot()
    def copyModsToProfileMenu(self) -> None:
        qDialog = SelectProfile()
        qDialog.exec()

        if qDialog.result() and qDialog.profile:
            self.copyModsToProfile(qDialog.profile)
    
    def copyModsToProfile(self, modsDestination: str) -> None:

        selectedItem: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if selectedItem is None:
            return

        copyingTo: qtw.QTreeWidgetItem = self.__findProfile(modsDestination)

        logging.info('Copying mods to %s', modsDestination)

        selectedItem.setSelected(False)

        copyingTo.setSelected(True)

        if self.isProfile(selectedItem):
            self.addMods(*[x.text(0) for x in self.__getMods(selectedItem)])
        else:
            self.addMods(selectedItem.text(0))
    
    @Slot()
    def menuAddProfile(self) -> None:
        '''
        Prompts the user to ask what the profile
        should be before running `addProfile()`

        If the user tries to input a duplicate profile name
        raise an error and try it again
        '''

        qDialog = InsertString('Profile name:')

        while True:
            
            qDialog.exec()

            if not qDialog.result():
                break

            elif qDialog.userInput:

                if qDialog.userInput not in self.__getProfiles():
                    self.addProfile(qDialog.userInput)
                    break
                else:
                    msg = Notice('A profile with this name already exists.', 
                                 'Error: Duplicate profile name')
                    msg.exec()

    def addProfile(self, *items: str, initalize: bool = False) -> None:
        '''
        Adds one or more new profiles to the list
        
        The initalize parameter is when the program loads from the json file
        '''

        profiles: list[str] = self.__getProfiles()

        for item in items:

            logging.info('Adding profile %s', item)

            if item in profiles:
                logging.warning('%s is a duplicate profile, not adding.', item)
                continue

            profile = qtw.QTreeWidgetItem([item, '0'])
            profile.setData(*DATA_PROFILE)
            self.addTopLevelItem(profile)
        
        if not initalize:
            ProfileManager.addProfile(*items)
    
    def isProfile(self, itemInQuestion: qtw.QTreeWidgetItem) -> bool:
        return itemInQuestion.data(0, ProfileRole.type) == DATA_PROFILE[2]

    @Slot()
    def deleteProfile(self) -> None:
        '''Deletes an existing profile'''

        toBeDeleted: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if toBeDeleted is None:
            return

        logging.info('Deleting profile %s', toBeDeleted.text(0))

        self.takeTopLevelItem(self.indexOfTopLevelItem(toBeDeleted))

        ProfileManager.removeProfile(toBeDeleted.text(0))
    
    @Slot()
    def editProfileMenu(self) -> None:

        qDialog = InsertString(qapp.translate('ProfileList', 'New profile name:'))

        while True:
            
            qDialog.exec()

            if not qDialog.result():
                break

            elif qDialog.userInput:

                if qDialog.userInput not in self.__getProfiles():
                    self.editProfile(qDialog.userInput)
                    break
                else:

                    logging.warning('A profile with the name %s already exists', qDialog.userInput)

                    msg = Notice(
                        message=
                        qapp.translate('ProfileList', 'A profile with that name already exists:') +
                        f' {qDialog.userInput}', 

                        headline=qapp.translate('ProfileList', 'Error: Duplicate profile name')
                    )
                    msg.exec()

    def editProfile(self, name: str) -> None:
        '''Changes the name of a profile'''

        profile: qtw.QTreeWidgetItem | None = self.__selectedItem()

        logging.info('Editing %s to %s', profile.text(0), name)

        ProfileManager.changeProfile(profile.text(0), name)

        profile.setText(0, name)

    @Slot()
    def copyProfile(self) -> None:

        profileToCopy: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if profileToCopy is None:
            return

        mods: list[qtw.QTreeWidgetItem] = self.__getMods(profileToCopy)

        logging.info('Copying %s', profileToCopy.text(0))

        modsToCopy: list[str] = [x.text(0) for x in mods]

        qDialog = InsertString(qapp.translate('ProfileList', 'New profile name:'))

        while True:

            qDialog.exec()

            if not qDialog.result():
                break

            elif qDialog.userInput:

                if qDialog.userInput not in self.__getProfiles():

                    self.addProfile(qDialog.userInput)

                    profileItem: qtw.QTreeWidgetItem = self.__findProfile(qDialog.userInput)

                    profileItem.setSelected(True)

                    profileToCopy.setSelected(False)

                    self.addMods(*modsToCopy)

                    break
                else:

                    logging.warning('A profile with the name %s already exists', qDialog.userInput)

                    msg = Notice(
                        message=
                        qapp.translate('ProfileList', 'A profile with that name already exists:') +
                        f' {qDialog.userInput}', 

                        headline=qapp.translate('ProfileList', 'Error: Duplicate profile name')
                    )
                    msg.exec()

    def unselectShortcut(self) -> None:
        toBeUnselected: qtw.QTreeWidgetItem | None = self.__selectedItem()
        if toBeUnselected:
            toBeUnselected.setSelected(False)

# EVENT OVERRIDES

    @override
    def mousePressEvent(self, event: qtg.QMouseEvent) -> None:

        if event.button() == qt.MouseButton.RightButton:

            self.clearSelection()

            selectedItem: qtw.QTreeWidgetItem | None = self.itemAt(event.pos())

            if selectedItem:

                selectedItem.setSelected(True)

                if self.isProfile(selectedItem):
                    self.profileRightclicked.emit()
                else:
                    self.modRightclicked.emit()

            self.menu.exec(qtg.QCursor.pos())

        elif event.button() == qt.MouseButton.LeftButton:

            if not self.itemAt(qtg.QCursor.pos()):
                self.clearSelection()

        return super().mousePressEvent(event)

    @override
    def keyPressEvent(self, event: qtg.QKeyEvent) -> None:

        selectedItem: qtw.QTreeWidgetItem | None = self.__selectedItem()

        if selectedItem is None:
            return

        if event.key() == qt.Key.Key_Delete or event.key() == qt.Key.Key_Backspace:

            if not self.isProfile(selectedItem):

                self.removeMods()

        elif event.key() == qt.Key.Key_Return:

            if self.isProfile(selectedItem):

                self.editProfileMenu()

        return super().keyPressEvent(event)
