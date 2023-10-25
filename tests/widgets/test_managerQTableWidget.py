import pytest
from pytestqt.qtbot import QtBot

from src.widgets.managerQTableWidget import ModListWidget
from src.constant_vars import ModType

MODS = (('mod1', ModType.mods, True, '2.3.0'),
        ('mod2', ModType.mods_override, True, 'None'),
        ('mod3', ModType.maps, None, '2.4.0'),
        )

@pytest.fixture(scope='module')
def create_QTable(createTemp_Config_ini: str, createTemp_Mod_ini: str) -> ModListWidget:

    widget = ModListWidget(createTemp_Mod_ini, createTemp_Config_ini)

    widget.addMod(name=MODS[0][0], type=MODS[0][1], enabled=MODS[0][2], version=MODS[0][3])
    widget.addMod(name=MODS[1][0], type=MODS[1][1], enabled=MODS[1][2], version=MODS[1][3])
    widget.addMod(name=MODS[2][0], type=MODS[2][1], enabled=MODS[2][2], version=MODS[2][3])

    return widget

def test_addMods(create_QTable: ModListWidget) -> None:

    assert create_QTable.rowCount() == 3
    assert create_QTable.getEnabledItem(2).text() == 'Disabled'
    assert create_QTable.getNameItem(0).text() == 'mod1'
    assert create_QTable.getTypeItem(0).text() == 'mods'
    assert create_QTable.getVersionItem(1).text() == '1.0.0'

def test_sort(create_QTable: ModListWidget) -> None:

    create_QTable.changeSortState(1)
    assert create_QTable.sortState['col'] == 1
    assert create_QTable.sortState['ascending'] == True
    create_QTable.changeSortState(1)
    assert create_QTable.sortState['ascending'] == False

def test_getSelectedNameItems(create_QTable: ModListWidget) -> None:

    create_QTable.selectAll()
    allNameItems = create_QTable.getSelectedNameItems()
    assert len(allNameItems) == 3

    names = (MODS[0][0], MODS[1][0], MODS[2][0])

    for item in allNameItems:
        assert item.text() in names

def test_getModTypeCount(create_QTable: ModListWidget) -> None:
    assert create_QTable.getModTypeCount(ModType.mods) == 1

def test_widget(qtbot: QtBot, create_QTable: ModListWidget) -> None:

    qtbot.addWidget(create_QTable)

    assert create_QTable.columnCount() == 4
    assert create_QTable.verticalHeader().isHidden() == True
    
