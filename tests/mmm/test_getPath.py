import os

import pytest

from src.save import OptionsManager
from src.constant_vars import ModType
from src.getPath import Pathing

DIR: str = os.path.abspath(os.path.join('tests', 'game_path'))

EXPECTED_OUTCOME: dict[int, str] = {
    0 : os.path.join('Maps', 'map mod'),
    1 : os.path.join('mods', 'reg mod'),
    2 : os.path.join('assets', 'mod_overrides', 'override mod')
}

PARAMETERS = ('type', 'modName', 'expected_outcome')

ARGS: list[tuple[ModType, str, str]] = [
    (ModType.maps, 'map mod', EXPECTED_OUTCOME[0]),
    (ModType.mods, 'reg mod', EXPECTED_OUTCOME[1]),
    (ModType.mods_override, 'override mod', EXPECTED_OUTCOME[2])
]

def test_getPath_ModDirs(createTemp_Config_ini: str, create_mod_dirs: str) -> None:
    OptionsManager(createTemp_Config_ini)

    assert Pathing.maps() == os.path.join(create_mod_dirs, 'Maps')
    assert Pathing.mods() == os.path.join(create_mod_dirs, 'mods')
    assert Pathing.mod_overrides() == os.path.join(create_mod_dirs, 'assets', 'mod_overrides')

@pytest.mark.parametrize(PARAMETERS, ARGS)
def test_getPath_Mod(type: str, modName: str, expected_outcome: str, createTemp_Config_ini: str, create_mod_dirs: str) -> None:
    OptionsManager(createTemp_Config_ini)

    assert Pathing.mod(type, modName) == os.path.join(create_mod_dirs, expected_outcome)
