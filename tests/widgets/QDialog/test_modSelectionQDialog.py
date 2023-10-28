from pytestqt.qtbot import QtBot

from src.widgets.QDialog.modSelectionQDialog import SelectMod
from src.save import OptionsManager

def test_dialog(qtbot: QtBot, createTemp_Mod_ini: str, createTemp_Config_ini: str, create_mod_dirs: str) -> None:
    options = OptionsManager(createTemp_Config_ini)
    options.setGamepath(create_mod_dirs)
    options.writeData()

    widget = SelectMod(createTemp_Mod_ini, createTemp_Config_ini)
    qtbot.addWidget(widget)

    assert widget.modList.count() == 3
    
    widget.modList.selectAll()

    widget.buttonBox.accepted.emit()

    assert widget.mods == [x.text() for x in widget.modList.selectedItems()]
    assert widget.result() == 1
