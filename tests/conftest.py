import tempfile
import os
import json
from configparser import ConfigParser

import pytest

from src.constant_vars import OptionKeys, ModKeys, ModType

@pytest.fixture(scope='session')
def getDir() -> str:
    return os.path.dirname(__file__)

@pytest.fixture(scope='module')
def createTemp_Mod_ini(getDir: str) -> str:
    with tempfile.NamedTemporaryFile('w', dir=getDir, suffix='.ini', delete=False) as tmp:
        tmp_filename = tmp.name
    
    config = ConfigParser()

    config.read(tmp_filename)

    for mod in (('super fun mod', ModType.maps.value, '3453'),
                ('best mod ever', ModType.mods_override.value, ''),
                ('make game easy mod', ModType.mods.value, '2523')):

        config.add_section(mod[0])

        config.set(mod[0], ModKeys.type.value, mod[1])
        config.set(mod[0], ModKeys.modworkshopid.value, mod[2])

    with open(tmp_filename, 'w') as f:
        config.write(f)

    yield tmp_filename

    os.remove(tmp_filename)

@pytest.fixture(scope='module')
def createTemp_Config_ini(getDir: str) -> str:
    with tempfile.NamedTemporaryFile('w', dir=getDir, suffix='.ini', delete=False) as tmp:
        tmp_filename = tmp.name

    config = ConfigParser()

    config.read(tmp_filename)

    config.add_section(OptionKeys.section.value)
    config.set(OptionKeys.section.value, OptionKeys.game_path.value, getDir)
    config.set(OptionKeys.section.value, OptionKeys.dispath.value, os.path.join(getDir, 'disabledMods'))

    with open(tmp_filename, 'w') as f:
        config.write(f)

    yield tmp_filename

    os.remove(tmp_filename)

@pytest.fixture(scope='module')
def createTemp_Profiles_ini(getDir: str) -> str:

    data = {'Awesome mods' : ['cool_beans', 'among us guards', 'make game easy']}

    with tempfile.NamedTemporaryFile('w', dir=getDir, suffix='.json', delete=False) as tmp:
        tmp_name = tmp.name

        tmp.write(json.dumps(data))

    yield tmp_name

    os.remove(tmp_name)
