from pytestqt.qtbot import QtBot

from src.widgets.QDialog.modSelectionQDialog import SelectMod

def test_dialog(qtbot: QtBot, createTemp_Mod_ini: str, createTemp_Config_ini: str, create_mod_dirs: str) -> None:
    widget = SelectMod()
    qtbot.addWidget(widget)

    assert widget.modList.count() == 3
    
    widget.modList.selectAll()

    widget.buttonBox.accepted.emit()

    assert widget.mods == [x.text() for x in widget.modList.selectedItems()]
    assert widget.result() == 1
