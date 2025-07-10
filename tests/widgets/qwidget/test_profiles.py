from pytestqt.qtbot import QtBot

from src.widgets.qwidget.mod_profile import ModProfile

def test_profiles(qtbot: QtBot, createTemp_Mod_ini: str, createTemp_Profiles_ini: str) -> None:

    widget = ModProfile()

    qtbot.addWidget(widget)
