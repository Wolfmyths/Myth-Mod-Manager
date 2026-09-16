from collections.abc import Generator
import tempfile
import os

import pytest

from src.helpers.options_manager import OptionsManager
from src.helpers import helper
from src.constant_vars import ModType

def test_getFileTypeDir() -> None:
    with tempfile.TemporaryDirectory() as tmp:

        assert helper.getFileType(tmp) == 'dir'

    with tempfile.NamedTemporaryFile('w', suffix='.zip') as tmp:

        assert helper.getFileType(tmp.name) == 'zip'
    
    with tempfile.NamedTemporaryFile('w', suffix='.rar') as tmp:

        assert helper.getFileType(tmp.name) == 'zip'

    with tempfile.NamedTemporaryFile('w', suffix='.7z') as tmp:

        assert helper.getFileType(tmp.name) == 'zip'

    with tempfile.NamedTemporaryFile('w', suffix='.invalidType') as tmp:

        assert helper.getFileType(tmp.name) == ''

@pytest.mark.parametrize(('modType', 'expected_outcome'),
                (
                            (ModType.maps, True),
                            (ModType.mods_override, True),
                            (ModType.mods, True),
                            ('fake mod type', False)))
def test_isTypeMod(modType: ModType, expected_outcome: bool) -> None:
    assert helper.isTypeMod(modType) == expected_outcome

@pytest.fixture(scope="module")
def begin_testing_createModDirs(createTemp_Config_ini: str) -> Generator[None]:
    old_ini = OptionsManager.file

    OptionsManager(createTemp_Config_ini)

    yield None

    OptionsManager(old_ini)

@pytest.mark.parametrize(
        'path',
        ['Maps', 'mods', os.path.join('assets', 'mod_overrides')])
def test_createModDirs(path: str, begin_testing_createModDirs: None, create_mod_dirs: str) -> None:  # pyright: ignore[reportUnusedParameter]
    helper.createModDirs()
    assert os.path.isdir(os.path.join(create_mod_dirs, path)) is True
