import os
import pytest
from typing import Generator

from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw

from src.widgets.qwidget.options import Options
from src.constant_vars import DARK, LIGHT, OptionKeys
from src.widgets.qwidget.options import OptionsManager

MOCK_GAMEPATH: str = os.path.abspath('path\\to\\gamepath')
MOCK_DISMODS: str = os.path.abspath('path\\to\\disabled\\mods')
MOCK_LANG: str = 'zh_CN'

@pytest.fixture(scope='module')
def create_Settings(createTemp_Config_ini: str) -> Generator:
    yield Options()

def test_Settings(create_Settings: Options) -> None:
    EXPECTED_SECTIONS = 5

    assert create_Settings.sectionsList.count() == EXPECTED_SECTIONS

    assert len(create_Settings.sections) == EXPECTED_SECTIONS

    for k in create_Settings.sections.keys():
        assert isinstance(create_Settings.sections[k], qtw.QWidget)

def test_gamePathChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.gamePathChanged(MOCK_GAMEPATH)

    assert create_Settings.optionChanged[OptionKeys.game_path] is True

def test_disPathChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.disPathChanged(MOCK_DISMODS)

    assert create_Settings.optionChanged[OptionKeys.dispath] is True

def test_themeChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.themeChanged(DARK)

    assert create_Settings.optionChanged[OptionKeys.color_theme] is True

def test_langChanged(create_Settings: Options) -> None:
    create_Settings.optionsGeneral.langChanged(MOCK_LANG)

    assert create_Settings.optionChanged[OptionKeys.lang] is True

def test_cancelChanges(create_Settings: Options) -> None:
    assert create_Settings.applyButton.isEnabled()

    create_Settings.cancelChanges()

    assert create_Settings.applyButton.isEnabled() is False

    assert sum(list(create_Settings.optionChanged.values())) == 0

def test_applySettings(qtbot: QtBot, create_Settings: Options, create_mod_dirs: str) -> None:
    newDisabledMods: str = os.path.join(create_mod_dirs, 'disabledMods')

    qtbot.addWidget(create_Settings)
    create_Settings.optionsGeneral.colorThemeDark.setChecked(True)
    create_Settings.optionsGeneral.disabledModDir.setText(newDisabledMods)
    create_Settings.optionsGeneral.gameDir.setText(create_mod_dirs)

    create_Settings.applyButton.setChecked(True)

    assert OptionsManager.getTheme() == LIGHT
    assert OptionsManager.getGamepath() == create_mod_dirs
    assert OptionsManager.getDispath() == newDisabledMods

    assert sum(list(create_Settings.optionChanged.values())) == 0
    assert create_Settings.applyButton.isEnabled() is False
