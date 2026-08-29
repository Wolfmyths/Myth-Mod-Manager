from typing import cast
from collections.abc import Generator

import pytest

from pytestqt.qtbot import QtBot

from src.constant_vars import ModType

from src.widgets.qwidget.tag_viewer import TagViewer
from src.widgets.qtable.mod_list_widget import ModListWidget

MODS = (
    ('mod1', ModType.mods, True, '2.3.0', ['cool']),
    ('mod2', ModType.mods_override, True, 'None', ['calm', 'cool']),
    ('mod3', ModType.maps, None, '2.4.0', None),
)

@pytest.fixture(scope='module')
def create_modListWidget(createTemp_Mod_ini: str, createTemp_Config_ini: str) -> Generator[ModListWidget]:  # pyright: ignore[reportUnusedParameter]
    widget = ModListWidget()

    widget.addMod(name=MODS[0][0], type=MODS[0][1], enabled=MODS[0][2], version=MODS[0][3], tags=MODS[0][4])
    widget.addMod(name=MODS[1][0], type=MODS[1][1], enabled=MODS[1][2], version=MODS[1][3], tags=MODS[1][4])
    widget.addMod(name=MODS[2][0], type=MODS[2][1], enabled=MODS[2][2], version=MODS[2][3], tags=MODS[2][4])  # pyright: ignore[reportArgumentType]

    yield widget

@pytest.fixture(scope='module')
def create_tagViewer(create_modListWidget: ModListWidget) -> Generator[TagViewer]:
    widget = TagViewer(create_modListWidget)
    yield widget

@pytest.mark.skip
def test_addTags(create_tagViewer: TagViewer) -> None:  # pyright: ignore[reportUnusedParameter]
    raise NotImplementedError

@pytest.mark.skip
def test_removeTags(create_tagViewer: TagViewer) -> None:  # pyright: ignore[reportUnusedParameter]
    raise NotImplementedError

def test_tagViewer(qtbot: QtBot, create_tagViewer: TagViewer) -> None:
    widget: TagViewer = create_tagViewer
    manager_table = cast(ModListWidget, widget.parent())

    qtbot.addWidget(manager_table)
    qtbot.addWidget(widget)
