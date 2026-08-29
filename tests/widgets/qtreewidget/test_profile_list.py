import pytest
from typing import Any
from collections.abc import Generator

from PySide6.QtWidgets import QTreeWidgetItem

from pytestqt.qtbot import QtBot

from src.widgets.qtreewidget.profile_list import ProfileList

@pytest.fixture(scope='module')
def create_ProfileList(createTemp_Profiles_ini: str) -> Generator[ProfileList]:  # pyright: ignore[reportUnusedParameter]
    yield ProfileList()

def test_modProfile(qtbot: QtBot, create_ProfileList: ProfileList) -> None:
    qtbot.addWidget(create_ProfileList)

    assert create_ProfileList.columnCount() == 2
    assert len(create_ProfileList.__getProfiles()) == 1  # pyright: ignore[reportPrivateUsage]
    profile: QTreeWidgetItem = create_ProfileList.__findProfile('Awesome mods')  # pyright: ignore[reportPrivateUsage]
    list_of_mods: list[QTreeWidgetItem] | None = create_ProfileList.__getMods(profile)  # pyright: ignore[reportPrivateUsage]
    assert len(list_of_mods) == 3

def test_addProfile(create_ProfileList: ProfileList) -> None:
    create_ProfileList.addProfile('newprofile')

    assert create_ProfileList.__findProfile('newprofile')  # pyright: ignore[reportPrivateUsage]
    assert len(create_ProfileList.__getProfiles()) == 2  # pyright: ignore[reportPrivateUsage]

def test_addMods(create_ProfileList: ProfileList) -> None:
    profile: QTreeWidgetItem = create_ProfileList.__findProfile('newprofile')  # pyright: ignore[reportPrivateUsage]
    profile.setSelected(True)

    create_ProfileList.addMods('super cool mod')
    profile.setSelected(False)

    assert len(create_ProfileList.__getMods(profile)) == 1  # pyright: ignore[reportPrivateUsage]

def test_isProfile(create_ProfileList: ProfileList) -> None:
    profile: QTreeWidgetItem = create_ProfileList.__findProfile('newprofile')  # pyright: ignore[reportPrivateUsage]
    mod: QTreeWidgetItem | Any = create_ProfileList.__getMods(profile)[0]  # pyright: ignore[reportPrivateUsage]

    assert create_ProfileList.isProfile(profile)
    assert not create_ProfileList.isProfile(mod)

def test_editProfile(create_ProfileList: ProfileList) -> None:
    profile: QTreeWidgetItem = create_ProfileList.__findProfile('newprofile')  # pyright: ignore[reportPrivateUsage]
    profile.setSelected(True)

    create_ProfileList.editProfile('editedprofile')
    profile.setSelected(False)

    assert profile.text(0) == 'editedprofile'

def test_copyModsToProfile(create_ProfileList: ProfileList) -> None:
    profile: QTreeWidgetItem = create_ProfileList.__findProfile('Awesome mods')  # pyright: ignore[reportPrivateUsage]
    copyToProfile: QTreeWidgetItem = create_ProfileList.__findProfile('editedprofile')  # pyright: ignore[reportPrivateUsage]
    profile.setSelected(True)
    create_ProfileList.copyModsToProfile('editedprofile')

    profile.setSelected(False)

    mods: list[str] = [x.text(0) for x in create_ProfileList.__getMods(copyToProfile)]  # pyright: ignore[reportPrivateUsage]
    assert len(mods) == 4

    for s in ['cool_beans', 'among us guards', 'make game easy']:
        assert s in mods

def test_deleteProfile(create_ProfileList: ProfileList) -> None:
    create_ProfileList.__findProfile('editedprofile').setSelected(True)  # pyright: ignore[reportPrivateUsage]
    create_ProfileList.deleteProfile()

    assert 'editedprofile' not in create_ProfileList.__getProfiles()  # pyright: ignore[reportPrivateUsage]

