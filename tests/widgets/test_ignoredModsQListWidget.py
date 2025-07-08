import pytest
from typing import Generator

from src.save import Save
from src.widgets.ignoredModsQListWidget import IgnoredMods

@pytest.fixture(scope='module')
def create_ignoredModList(createTemp_Mod_ini: str) -> Generator:
    widget = IgnoredMods()
    yield widget
    widget.deleteLater()

def test_refreshList(create_ignoredModList: IgnoredMods) -> None:
    
    Save.setIgnored('super fun mod', True)
    Save.saveJSON()

    create_ignoredModList.refreshList()

    assert create_ignoredModList.count() == 1