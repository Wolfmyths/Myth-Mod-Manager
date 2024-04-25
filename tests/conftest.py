from typing import Generator
import tempfile
import os
import json
from configparser import ConfigParser

import pytest

from src.constant_vars import OptionKeys, ModKeys, ModType, LIGHT

@pytest.fixture(scope='session')
def getDir() -> str:
    return os.path.dirname(__file__)

@pytest.fixture
def create_mod_dirs() -> Generator:
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.makedirs(os.path.join(tmp_dir, 'mods', 'make game easy mod'))
        os.makedirs(os.path.join(tmp_dir, 'assets', 'mod_overrides', 'best mod ever'))
        os.makedirs(os.path.join(tmp_dir, 'maps', 'super fun mod'))
        os.mkdir(os.path.join(tmp_dir, 'disabledMods'))
        
        yield tmp_dir

@pytest.fixture(scope='module')
def createTemp_Mod_ini() -> Generator:
    data = {'super fun mod' : {ModKeys.type.value : ModType.maps.value,
                               ModKeys.modworkshopid.value : '3453',
                               ModKeys.enabled.value : True,
                               ModKeys.ignored.value : False},

            'best mod ever' : {ModKeys.type.value : ModType.mods_override.value,
                               ModKeys.modworkshopid.value : '',
                               ModKeys.enabled.value : True,
                               ModKeys.ignored.value : False},
            
            'make game easy mod' : {ModKeys.type.value : ModType.mods.value,
                                ModKeys.modworkshopid.value : '2523',
                                ModKeys.enabled.value : True,
                                ModKeys.ignored.value : False}
            }

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name = tmp.name

        tmp.write(json.dumps(data))

    yield tmp_name

    os.remove(tmp_name)

@pytest.fixture(scope='module')
def createTemp_Config_ini(getDir: str) -> Generator:
    with tempfile.NamedTemporaryFile('w', suffix='.ini', delete=False) as tmp:
        tmp_filename = tmp.name

    config = ConfigParser()

    config.read(tmp_filename)

    config.add_section(OptionKeys.section.value)
    config.set(OptionKeys.section.value, OptionKeys.color_theme.value, LIGHT)
    config.set(OptionKeys.section.value, OptionKeys.game_path.value, os.path.join(getDir, 'game_path'))
    config.set(OptionKeys.section.value, OptionKeys.dispath.value, os.path.join(getDir, 'game_path', 'disabledMods'))
    config.set(OptionKeys.section.value, OptionKeys.mmm_update_alert.value, str(False))

    with open(tmp_filename, 'w') as f:
        config.write(f)

    yield tmp_filename

    os.remove(tmp_filename)

@pytest.fixture(scope='module')
def createTemp_Profiles_ini() -> Generator:

    data = {'Awesome mods' : ['cool_beans', 'among us guards', 'make game easy']}

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name = tmp.name

        tmp.write(json.dumps(data))

    yield tmp_name

    os.remove(tmp_name)

@pytest.fixture(scope='module')
def createTemp_externalShortcuts_ini() -> Generator:

    data = {'shortcuts' : ['C:\\path\\program.exe', 'D:\\path\\payday.exe', 'C:\\path\\map_builder.exe']}

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name = tmp.name

        tmp.write(json.dumps(data))

    yield tmp_name

    os.remove(tmp_name)
