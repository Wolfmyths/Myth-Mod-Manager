import os

import pytest
from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

from src.settings import Options
from src.constant_vars import DARK, LIGHT, OptionKeys

MOCK_DISMODS = os.path.abspath('path\\to\\disabled\\mods')
MOCK_GAMEPATH = os.path.abspath('path\\to\\gamepath')

@pytest.fixture(scope='module')
def create_Settings(createTemp_Config_ini: str) -> Options:
    return Options(createTemp_Config_ini)

def test_Settings(qtbot: QtBot, create_Settings: Options) -> None:
    qtbot.addWidget(create_Settings)

    assert create_Settings.sectionsList.count() == 4

    assert len(create_Settings.sections) == 4

    for k in create_Settings.sections.keys():
        assert isinstance(create_Settings.sections[k], qtw.QWidget)

def test_gamePathChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.gamePathChanged(MOCK_GAMEPATH)

    assert create_Settings.optionChanged[OptionKeys.game_path] == True

def test_disPathChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.disPathChanged(MOCK_DISMODS)

    assert create_Settings.optionChanged[OptionKeys.dispath] == True

def test_themeChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.themeChanged(DARK)

    assert create_Settings.optionChanged[OptionKeys.color_theme] == True

def test_cancelChanges(create_Settings: Options) -> None:
    assert create_Settings.applyButton.isEnabled()

    create_Settings.cancelChanges()

    assert create_Settings.applyButton.isEnabled() == False

    assert sum(list(create_Settings.optionChanged.values())) == 0

def test_applySettings(qtbot: QtBot, create_Settings: Options) -> None:
    qtbot.addWidget(create_Settings)
    qtbot.mouseClick(create_Settings.optionsGeneral.colorThemeDark, qt.MouseButton.LeftButton)

    create_Settings.optionsGeneral.gameDir.setText(MOCK_GAMEPATH)
    create_Settings.optionsGeneral.disabledModDir.setText(MOCK_DISMODS)
    
    qtbot.mouseClick(create_Settings.applyButton, qt.MouseButton.LeftButton)

    assert create_Settings.optionsManager.getTheme() == DARK
    assert create_Settings.optionsManager.getGamepath() == MOCK_GAMEPATH
    assert create_Settings.optionsManager.getDispath() == MOCK_DISMODS

    assert sum(list(create_Settings.optionChanged.values())) == 0
    assert create_Settings.applyButton.isEnabled() == False
