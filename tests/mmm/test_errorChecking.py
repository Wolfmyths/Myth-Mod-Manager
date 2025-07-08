import tempfile
import os
import stat

import pytest
from semantic_version import Version

from src.save import OptionsManager
import src.errorChecking
from src.constant_vars import ModType

def test_getFileType() -> None:

    with tempfile.TemporaryDirectory() as tmp:

        assert src.errorChecking.getFileType(tmp) == 'dir'

    with tempfile.TemporaryFile('w', suffix='.zip') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'
    
    with tempfile.TemporaryFile('w', suffix='.rar') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.7z') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.invalidType') as tmp:

        assert src.errorChecking.getFileType(tmp.name) is False

def test_permissionCheck() -> None:

    with tempfile.TemporaryDirectory() as tmp:

        os.chmod(tmp, stat.S_IREAD)

        assert src.errorChecking.permissionCheck(tmp) == 0
        assert str(oct(os.stat(tmp).st_mode))[-3:] == '777'
        assert src.errorChecking.permissionCheck(tmp) == 1

@pytest.mark.parametrize(('version', 'expected_outcome'),
                         (
                            (Version(major=1, minor=0, patch=0), False),
                            (Version(major=1, minor=0, patch=0, prerelease='1'), True)
                         )
                        )
def test_isPrerelease(version: Version, expected_outcome: bool) -> None:
    assert src.errorChecking.isPrerelease(version) == expected_outcome

@pytest.mark.parametrize(('modType', 'expected_outcome'),
                         (
                            (ModType.maps, True),
                            (ModType.mods_override, True),
                            (ModType.mods, True),
                            ('fake mod type', False)
                         )
                        )
def test_isTypeMod(modType: ModType, expected_outcome: bool) -> None:
    assert src.errorChecking.isTypeMod(modType) == expected_outcome

@pytest.fixture(scope="module")
def begin_testing_createModDirs(createTemp_Config_ini: str) -> None:
    OptionsManager(createTemp_Config_ini)
    src.errorChecking.createModDirs()

@pytest.mark.parametrize(
        'path',
        ['Maps', 'mods', os.path.join('assets', 'mod_overrides')]
)
def test_createModDirs(path: str, begin_testing_createModDirs: None, create_mod_dirs: str) -> None:
    assert os.path.isdir(os.path.join(create_mod_dirs, path)) is True
