from pytestqt.qtbot import QtBot

from src.widgets.aboutQWidget import About
from src.constant_vars import DARK, LIGHT, MODWORKSHOP_LOGO_W, GITHUB_LOGO_W, KOFI_LOGO_B, MODWORKSHOP_LOGO_B, GITHUB_LOGO_B

def test_about(qtbot: QtBot, createTemp_Config_ini: str) -> None:
    widget = About(createTemp_Config_ini)

    qtbot.addWidget(widget)

    assert widget.kofiIcon == KOFI_LOGO_B
    assert widget.githubIcon == GITHUB_LOGO_B
    assert widget.modworkshopIcon == MODWORKSHOP_LOGO_B

    widget.options.setTheme(DARK)

    widget.updateIcons(DARK)

    assert widget.githubIcon == GITHUB_LOGO_W
    assert widget.modworkshopIcon == MODWORKSHOP_LOGO_W

    widget.updateIcons(LIGHT)

    assert widget.githubIcon == GITHUB_LOGO_B
    assert widget.modworkshopIcon == MODWORKSHOP_LOGO_B