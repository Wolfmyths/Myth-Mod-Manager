import pytest
from pytestqt.qtbot import QtBot

from src.widgets.modInfoQWidget import ModInfo

# ModInfo feature not implemented yet
@pytest.mark.skip
def test_modInfo(qtbot: QtBot) -> None:
    widget = ModInfo()
    qtbot.addWidget(widget)
