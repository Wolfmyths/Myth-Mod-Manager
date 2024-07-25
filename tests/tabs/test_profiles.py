from pytestqt.qtbot import QtBot

from src.profiles import modProfile

def test_profiles(qtbot: QtBot, createTemp_Mod_ini: str, createTemp_Profiles_ini: str) -> None:

    widget = modProfile(createTemp_Mod_ini, createTemp_Profiles_ini)

    qtbot.addWidget(widget)
