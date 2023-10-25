import pytest
from pytestqt.qtbot import QtBot

from src.widgets.ignoredModsQListWidget import IgnoredMods

@pytest.fixture(scope='module')
def create_ignoredModList(createTemp_Mod_ini: str) -> IgnoredMods:
    return IgnoredMods(savePath=createTemp_Mod_ini)

def test_ignoredModList(qtbot: QtBot, create_ignoredModList: IgnoredMods) -> None:
    qtbot.addWidget(create_ignoredModList)

def test_refreshList(create_ignoredModList: IgnoredMods) -> None:
    
    create_ignoredModList.saveManager.setIgnored('super fun mod', True)

    create_ignoredModList.refreshList()

    assert create_ignoredModList.count() == 1