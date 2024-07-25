from PySide6.QtCore import Qt as qt

from pytestqt.qtbot import QtBot

from src.manager import ModManager

from src.constant_vars import ModType

def test_manager(qtbot: QtBot, createTemp_Mod_ini: str, createTemp_Config_ini: str):

    widget = ModManager(createTemp_Mod_ini, createTemp_Config_ini)
    qtbot.addWidget(widget)

    modsCount = widget.modsTable.getModTypeCount(ModType.mods)
    overrideCount = widget.modsTable.getModTypeCount(ModType.mods_override)
    mapsCount = widget.modsTable.getModTypeCount(ModType.maps)

    assert widget.totalModsLabel.text() == f'Total Mods: {widget.modsTable.rowCount()}'
    assert widget.modsLabel.text() == f'Mods: {modsCount}'
    assert widget.overrideLabel.text() == f'Mod_Overrides: {overrideCount}'
    assert widget.mapsLabel.text() == f'Maps: {mapsCount}'

    widget.modsTable.addMod(name='testing', type=ModType.mods, enabled=True, version='None')
    widget.modsTable.addMod(name='testing1', type=ModType.maps, enabled=False, version='1.3.2')
    widget.modsTable.addMod(name='testing2', type=ModType.mods_override, enabled=True, version='4.2.1')

    assert widget.totalModsLabel.text() == f'Total Mods: {widget.modsTable.rowCount()}'
    assert widget.modsLabel.text() == f'Mods: {modsCount + 1}'
    assert widget.overrideLabel.text() == f'Mod_Overrides: {overrideCount + 1}'
    assert widget.mapsLabel.text() == f'Maps: {mapsCount + 1}'

    widget.selectAllShortCut.activated.emit()

    assert len(widget.modsTable.getSelectedNameItems()) == widget.modsTable.rowCount()

    widget.deselectAllShortCut.activated.emit()

    assert len(widget.modsTable.selectedItems()) == 0
