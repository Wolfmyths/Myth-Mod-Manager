from collections.abc import Generator
import tempfile
import os
import json
from configparser import ConfigParser

import pytest

from src.helpers.profile_manager import ProfileManager
from src.helpers.tools_manager import ToolJSON
from src.helpers.save_manager import Save
from src.helpers.options_manager import OptionsManager
from src.constant_vars import OptionKeys, ModKeys, ModType, LIGHT

MOCK_MOD_NAME_1 = 'make game easy mod'
MOCK_MOD_NAME_2 = 'best mod ever'
MOCK_MOD_NAME_3 = 'super fun mod'

@pytest.fixture(scope='module')
def create_mod_dirs() -> Generator[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.makedirs(os.path.join(tmp_dir, 'mods', MOCK_MOD_NAME_1))
        os.makedirs(os.path.join(tmp_dir, 'assets', 'mod_overrides', MOCK_MOD_NAME_2))
        os.makedirs(os.path.join(tmp_dir, 'maps', MOCK_MOD_NAME_3))
        os.mkdir(os.path.join(tmp_dir, 'disabledMods'))
        os.mkdir(os.path.join(tmp_dir, 'newDisabledMods'))

        yield tmp_dir

@pytest.fixture(scope='module')
def createTemp_Mod_ini() -> Generator[str]:
    data: dict[str, ModType | str | bool] = {  # pyright: ignore[reportAssignmentType]
        MOCK_MOD_NAME_3 : {
            ModKeys.type.value : ModType.maps.value,
            ModKeys.modworkshopid.value : '3453',
            ModKeys.enabled.value : True,
            ModKeys.ignored.value : False
        },

        MOCK_MOD_NAME_2 : {
            ModKeys.type.value : ModType.mods_override.value,
            ModKeys.modworkshopid.value : '',
            ModKeys.enabled.value : True,
            ModKeys.ignored.value : False
        },
            
        MOCK_MOD_NAME_1 : {
            ModKeys.type.value : ModType.mods.value,
            ModKeys.modworkshopid.value : '2523',
            ModKeys.enabled.value : True,
            ModKeys.ignored.value : False
        }
    }

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name: str = tmp.name

        tmp.write(json.dumps(data))

    Save(tmp_name)

    yield tmp_name

    Save._file = {}  # pyright: ignore[reportPrivateUsage]
    Save._path = ''  # pyright: ignore[reportPrivateUsage]

    os.remove(tmp_name)

@pytest.fixture(scope='module')
def createTemp_Config_ini(create_mod_dirs: str) -> Generator[str]:
    with tempfile.NamedTemporaryFile('w', suffix='.ini', delete=False) as tmp:
        tmp_filename: str = tmp.name

    config = ConfigParser()

    config.read(tmp_filename)

    config.add_section(OptionKeys.section.value)
    config.set(OptionKeys.section.value, OptionKeys.color_theme.value, LIGHT)
    config.set(OptionKeys.section.value, OptionKeys.game_path.value, os.path.join(create_mod_dirs, "PAYDAY2.exe"))
    config.set(OptionKeys.section.value, OptionKeys.dispath.value, os.path.join(create_mod_dirs, 'disabledMods'))
    config.set(OptionKeys.section.value, OptionKeys.mmm_update_alert.value, str(False))

    with open(tmp_filename, 'w') as f:
        config.write(f)

    OptionsManager.config = config
    OptionsManager.file = tmp_filename

    yield tmp_filename

    OptionsManager.config = ConfigParser()
    OptionsManager.file = ''

    os.remove(tmp_filename)

@pytest.fixture(scope='module')
def createTemp_Profiles_ini() -> Generator[str]:

    data: dict[str, list[str]] = {'Awesome mods' : ['cool_beans', 'among us guards', 'make game easy']}

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name: str = tmp.name

        tmp.write(json.dumps(data))

    ProfileManager(tmp_name)

    yield tmp_name

    ProfileManager._file = {}  # pyright: ignore[reportPrivateUsage]
    ProfileManager._path = ''  # pyright: ignore[reportPrivateUsage]

    os.remove(tmp_name)

@pytest.fixture(scope='module')
def createTemp_externalShortcuts_ini() -> Generator[str]:

    data: dict[str, list[str]] = {'shortcuts' : [
        os.path.abspath(os.path.join("path", "program.exe")),
        os.path.abspath(os.path.join('D:', 'path', 'payday.exe')),
        os.path.abspath(os.path.join('path', 'map_builder.exe'))]}

    with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tmp:
        tmp_name: str = tmp.name

        tmp.write(json.dumps(data))

    ToolJSON(tmp_name)

    yield tmp_name

    ToolJSON._file = {}  # pyright: ignore[reportPrivateUsage]
    ToolJSON._path = ''  # pyright: ignore[reportPrivateUsage]

    os.remove(tmp_name)
