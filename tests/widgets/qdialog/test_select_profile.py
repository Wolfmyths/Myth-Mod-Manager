from pytestqt.qtbot import QtBot

from src.widgets.qdialog.select_profile import SelectProfile

def test_dialog(qtbot: QtBot, createTemp_Profiles_ini: str) -> None:  # pyright: ignore[reportUnusedParameter]
    widget = SelectProfile()
    qtbot.addWidget(widget)

    assert widget.profileList.count() == 1
    
    widget.profileList.item(0).setSelected(True)

    widget.buttonBox.accepted.emit()

    assert widget.result() == 1
    assert widget.profile == 'Awesome mods'
