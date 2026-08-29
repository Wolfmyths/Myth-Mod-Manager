import tempfile
import os

import pytest

from src.helpers.options_manager import OptionsManager
import src.helpers.helper
from src.constant_vars import ModType

def test_getFileType() -> None:

    with tempfile.TemporaryDirectory() as tmp:

        assert src.helpers.helper.getFileType(tmp) == 'dir'

    with tempfile.TemporaryFile('w', suffix='.zip') as tmp:

        assert src.helpers.helper.getFileType(tmp.name) == 'zip'
    
    with tempfile.TemporaryFile('w', suffix='.rar') as tmp:

        assert src.helpers.helper.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.7z') as tmp:

        assert src.helpers.helper.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.invalidType') as tmp:

        assert src.helpers.helper.getFileType(tmp.name) == ''

@pytest.mark.parametrize(('modType', 'expected_outcome'),
                         (
                            (ModType.maps, True),
                            (ModType.mods_override, True),
                            (ModType.mods, True),
                            ('fake mod type', False)
                         )
                        )
def test_isTypeMod(modType: ModType, expected_outcome: bool) -> None:
    assert src.helpers.helper.isTypeMod(modType) == expected_outcome

@pytest.fixture(scope="module")
def begin_testing_createModDirs(createTemp_Config_ini: str) -> None:
    OptionsManager(createTemp_Config_ini)
    src.helpers.helper.createModDirs()

@pytest.mark.parametrize(
        'path',
        ['Maps', 'mods', os.path.join('assets', 'mod_overrides')]
)
def test_createModDirs(path: str, begin_testing_createModDirs: None, create_mod_dirs: str) -> None:  # pyright: ignore[reportUnusedParameter]
    assert os.path.isdir(os.path.join(create_mod_dirs, path)) is True
