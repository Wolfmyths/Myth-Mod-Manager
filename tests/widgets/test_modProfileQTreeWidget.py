import pytest
from pytestqt.qtbot import QtBot

from src.widgets.modProfileQTreeWidget import ProfileList

@pytest.fixture(scope='module')
def create_ProfileList(createTemp_Profiles_ini: str) -> ProfileList:
    return ProfileList(profilePath = createTemp_Profiles_ini)

def test_modProfile(qtbot: QtBot, create_ProfileList: ProfileList) -> None:
    qtbot.addWidget(create_ProfileList)

    assert create_ProfileList.columnCount() == 2
    assert len(create_ProfileList.__getProfiles()) == 1
    profile = create_ProfileList.__findProfile('Awesome mods')
    list_of_mods = create_ProfileList.__getMods(profile)
    assert len(list_of_mods) == 3

def test_addProfile(create_ProfileList: ProfileList) -> None:
    create_ProfileList.addProfile('newprofile')

    assert create_ProfileList.__findProfile('newprofile')
    assert len(create_ProfileList.__getProfiles()) == 2

def test_addMods(create_ProfileList: ProfileList) -> None:
    profile = create_ProfileList.__findProfile('newprofile')
    profile.setSelected(True)

    create_ProfileList.addMods('super cool mod')
    profile.setSelected(False)

    assert len(create_ProfileList.__getMods(profile)) == 1

def test_isProfile(create_ProfileList: ProfileList) -> None:
    profile = create_ProfileList.__findProfile('newprofile')
    mod = create_ProfileList.__getMods(profile)[0]

    assert create_ProfileList.isProfile(profile)
    assert not create_ProfileList.isProfile(mod)

def test_editProfile(create_ProfileList: ProfileList) -> None:
    profile = create_ProfileList.__findProfile('newprofile')
    profile.setSelected(True)

    create_ProfileList.editProfile('editedprofile')
    profile.setSelected(False)

    assert profile.text(0) == 'editedprofile'

def test_copyModsToProfile(create_ProfileList: ProfileList) -> None:
    profile = create_ProfileList.__findProfile('Awesome mods')
    copyToProfile = create_ProfileList.__findProfile('editedprofile')
    profile.setSelected(True)
    create_ProfileList.copyModsToProfile('editedprofile')

    profile.setSelected(False)

    mods = [x.text(0) for x in create_ProfileList.__getMods(copyToProfile)]
    assert len(mods) == 4

    for s in ['cool_beans', 'among us guards', 'make game easy']:
        assert s in mods

def test_deleteProfile(create_ProfileList: ProfileList) -> None:
    create_ProfileList.__findProfile('editedprofile').setSelected(True)
    create_ProfileList.deleteProfile()

    assert not 'editedprofile' in create_ProfileList.__getProfiles()

