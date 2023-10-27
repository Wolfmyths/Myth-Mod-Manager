import os

from pytestqt.qtbot import QtBot

from PySide6.QtCore import QUrl
import PySide6.QtWidgets as qtw

from src.widgets.QDialog.newModQDialog import newModLocation
from src.constant_vars import ModType

def test_dialog(qtbot: QtBot, create_mod_dirs: str) -> None:
    widget = newModLocation(*[QUrl(x) for x in os.listdir(os.path.join(create_mod_dirs, 'mods'))])
    qtbot.addWidget(widget)

    assert len(widget.findChildren(qtw.QGroupBox)) == 3

    radioButton0: qtw.QRadioButton = widget.findChild(qtw.QRadioButton, f'super fun mod {ModType.mods}')
    radioButton0.click()

    assert widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).isEnabled() == False

    radioButton1: qtw.QRadioButton = widget.findChild(qtw.QRadioButton, f'best mod ever {ModType.mods_override}')
    radioButton1.click()

    radioButton2: qtw.QRadioButton = widget.findChild(qtw.QRadioButton, f'make game easy mod {ModType.maps}')
    radioButton2.click()

    assert widget.buttonBox.button(qtw.QDialogButtonBox.StandardButton.Ok).isEnabled()

    widget.buttonBox.accepted.emit()

    assert widget.typeDict == {'super fun mod' : ModType.mods,
                               'best mod ever' : ModType.mods_override,
                               'make game easy mod': ModType.maps}
