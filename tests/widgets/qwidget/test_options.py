import os
import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt

from src.widgets.qwidget.options import Options
from src.constant_vars import DARK, LIGHT, OptionKeys
from src.helpers.options_manager import OptionsManager

MOCK_GAMEPATH: str = os.path.abspath('path\\to\\gamepath')
MOCK_DISMODS: str = os.path.abspath('path\\to\\disabled\\mods')
MOCK_LANG: str = 'zh_CN'

@pytest.fixture(scope='module')
def create_Settings(createTemp_Config_ini: str) -> Generator[Options]:  # pyright: ignore[reportUnusedParameter]
    options = Options()
    
    yield options

    options.deleteLater()

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
    language_combobox = create_Settings.optionsGeneral.language
    original_text: str = language_combobox.currentText()

    language_combobox.setEditable(True)
    language_combobox.setCurrentText(MOCK_LANG)

    assert create_Settings.optionChanged[OptionKeys.lang] is True

    language_combobox.setCurrentText(original_text)
    language_combobox.setEditable(False)

def test_launchParamsChanged(qtbot: QtBot, create_Settings: Options) -> None:
    launch_params = create_Settings.launchparams
    MOCK_TEXT = "t"

    # Test QCheckBoxes
    for check_box in launch_params.findChildren(qtw.QCheckBox):
        assert check_box.property("param") is not None

        check_box.click()
        assert create_Settings.optionChanged[OptionKeys.launch_parameters] is True
        check_box.click()
        assert create_Settings.optionChanged[OptionKeys.launch_parameters] is False
    
    # Test QLineEdits
    for line_edit in (launch_params.customLineEdit, launch_params.dLineEdit, launch_params.oLineEdit):
        line_edit.setFocus()
        qtbot.keyClick(line_edit, MOCK_TEXT)  # pyright: ignore[reportUnknownMemberType]
        assert create_Settings.optionChanged[OptionKeys.launch_parameters] is True
        qtbot.keyClick(line_edit, Qt.Key.Key_Backspace)  # pyright: ignore[reportUnknownMemberType]
        assert create_Settings.optionChanged[OptionKeys.launch_parameters] is False

def test_cancelChanges(create_Settings: Options) -> None:
    assert create_Settings.applyButton.isEnabled()

    create_Settings.cancelButton.click()

    assert create_Settings.applyButton.isEnabled() is False

    assert sum(list(create_Settings.optionChanged.values())) == 0

def test_applySettings(qtbot: QtBot, create_Settings: Options, create_mod_dirs: str) -> None:
    newDisabledMods: str = os.path.join(create_mod_dirs, 'disabledMods')

    qtbot.addWidget(create_Settings)
    create_Settings.optionsGeneral.colorThemeDark.setChecked(True)
    create_Settings.optionsGeneral.disabledModDir.setText(newDisabledMods)
    create_Settings.optionsGeneral.gameDir.setText(create_mod_dirs)

    create_Settings.applyButton.click()

    assert OptionsManager.getTheme() == LIGHT
    assert OptionsManager.getGamepath() == create_mod_dirs
    assert OptionsManager.getDispath() == newDisabledMods

    assert sum(list(create_Settings.optionChanged.values())) == 0
    assert create_Settings.applyButton.isEnabled() is False
