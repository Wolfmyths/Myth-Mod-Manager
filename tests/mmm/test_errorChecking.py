import tempfile
import os
import stat

import pytest
from semantic_version import Version

import src.errorChecking
from src.constant_vars import ModType

def test_getFileType():

    with tempfile.TemporaryDirectory() as tmp:

        assert src.errorChecking.getFileType(tmp) == 'dir'

    with tempfile.TemporaryFile('w', suffix='.zip') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'
    
    with tempfile.TemporaryFile('w', suffix='.rar') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.7z') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == 'zip'

    with tempfile.TemporaryFile('w', suffix='.invalidType') as tmp:

        assert src.errorChecking.getFileType(tmp.name) == False

def test_permissionCheck():

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
def test_isPrerelease(version: Version, expected_outcome: bool):
    assert src.errorChecking.isPrerelease(version) == expected_outcome

@pytest.mark.parametrize(('modType', 'expected_outcome'),
                         (
                            (ModType.maps, True),
                            (ModType.mods_override, True),
                            (ModType.mods, True),
                            ('fake mod type', False)
                         )
                        )
def test_isTypeMod(modType: ModType, expected_outcome: bool):
    assert src.errorChecking.isTypeMod(modType) == expected_outcome


@pytest.fixture
def begin_testing_createModDirs(createTemp_Config_ini) -> None:
    src.errorChecking.createModDirs(createTemp_Config_ini)

# TODO: This test is actually not tested throughly because errorchecking doesn't actually
# create the neccessary folders becuase other tests need them.
# We need a way to make this function point to a seperate environment like %TEMP% to do safe testing there
@pytest.mark.parametrize('path', (
                                    os.path.join('Maps'),
                                    os.path.join('mods'),
                                    os.path.join('assets', 'mod_overrides')
                                 )
                        )
def test_createModDirs(begin_testing_createModDirs: None, getDir: str, path: str):
    assert os.path.isdir(os.path.join(getDir, 'game_path', path)) == True
