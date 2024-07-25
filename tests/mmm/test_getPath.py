import os

import pytest

from src.constant_vars import ModType
from src.getPath import Pathing

DIR = os.path.abspath(os.path.join('tests', 'game_path'))

EXPECTED_OUTCOME = {
    0 : os.path.join(DIR, 'Maps', 'map mod'),
    1 : os.path.join(DIR, 'mods', 'reg mod'),
    2 : os.path.join(DIR, 'assets', 'mod_overrides', 'override mod')
}

PARAMETERS = ('type', 'modName', 'expected_outcome')

ARGS = [
    (ModType.maps, 'map mod', EXPECTED_OUTCOME[0]),
    (ModType.mods, 'reg mod', EXPECTED_OUTCOME[1]),
    (ModType.mods_override, 'override mod', EXPECTED_OUTCOME[2])
]

def test_getPath_ModDirs(createTemp_Config_ini: str, getDir: str):
    path = Pathing(createTemp_Config_ini)

    game_path = os.path.join(getDir, 'game_path')

    assert path.maps() == os.path.join(game_path, 'Maps')
    assert path.mods() == os.path.join(game_path, 'mods')
    assert path.mod_overrides() == os.path.join(game_path, 'assets', 'mod_overrides')

@pytest.mark.parametrize(PARAMETERS, ARGS)
def test_getPath_Mod(type: str, modName: str, expected_outcome: str, createTemp_Config_ini: str):
    path = Pathing(createTemp_Config_ini)

    assert path.mod(type, modName) == expected_outcome
