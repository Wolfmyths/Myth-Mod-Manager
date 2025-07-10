import os
import sys
from enum import StrEnum, auto

import semantic_version

##
## THIS FILE IS PLACED NEXT TO __main__ FOR FILE PATH REASONS
##

class ModType(StrEnum):
    '''
    Types of PAYDAY 2 mods 
    in reference to where they're installed.
    '''

    mods          = auto()
    mods_override = auto()
    maps          = auto()

    def all_types() -> list[str]:
        return [enum.value for enum in ModType]

class ModKeys(StrEnum):
    '''Keys that a mod has in `MOD_CONFIG`'''
    enabled       = auto()
    type          = auto()
    modworkshopid = auto()
    ignored       = auto()
    tags          = auto()

class OptionKeys(StrEnum):
    '''Option's keys in `OPTIONS_CONFIG`'''

    section          = 'OPTIONS' # Main section

    game_path         = auto()
    dispath          = 'disabled-mods'
    color_theme       = auto()
    windowsize_w      = auto()
    windowsize_h      = auto()
    mmm_update_alert  = auto()
    lang              = auto()
    launch_parameters = auto()

    def all_keys() -> list[str]:
        # Splice removes section key
        return [enum.value for enum in OptionKeys][1:]

class ProfileRole():

    parent    = 33 # Role ID for an item's parent
    type      = 32 # Role ID for an item's type
    installed = 34 # Role ID if a mod is installed or not

class ModRole():
    tags = 33 # Role ID for a mod's tags

# Lang map string to code
LANG_STR_TO_CODE: dict[str:str] = {
    'Deutsch'            : 'de_DE',
    'English'            : 'en_US',
    'Español (españa)'   : 'es_ES',
    'Français'           : 'fr_FR',
    'Italiano'           : 'it_IT',
    '日本語'              : 'ja_JP',
    '한국인'              : 'ko_KR',
    'Nederlands'         : 'nl_NL',
    'Polski'             : 'pl_PL',
    'Português (Brasil)' : 'pt_BR',
    'Русский'            : 'ru_RU',
    '中文（简体）'        : 'zh_CN'
}

# Lang code map code to string
LANG_CODE_TO_STR: dict[str:str] = {x:y for y,x in LANG_STR_TO_CODE.items()}

# Detection if the program is being run through an exe or the script
IS_SCRIPT = not getattr(sys, 'frozen', False)

# Root Path
ROOT_PATH = os.path.abspath(os.getcwd())

# Logs Folder Path
LOGS_PATH = os.path.join(ROOT_PATH, 'logs')
MAX_LOGS = 10

# Lang Folder Path
LANG_FOLDER_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lang')

# Icon Path
ICON = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icon.ico')

# File names
MOD_CONFIG = 'mods.json'
OPTIONS_CONFIG = 'config.ini'
PROFILES_JSON = 'profiles.json'
TOOLS_JSON = 'externalshortcuts.json'
START_PAYDAY = 'runGame.bat'
OLD_EXE = 'Myth Mod Manager.exe (Old)' if sys.platform.startswith('win') else 'Myth Mod Manager (old)'
DISABLED_MODS = 'disabled-mods'
BACKUP_MODS = 'backup mods'

# Graphics names
MODWORKSHOP_LOGO_W = 'mws_logo_white.svg'
MODWORKSHOP_LOGO_B = 'mws_logo_black.svg'
GITHUB_LOGO_W = 'github-mark-white.svg'
GITHUB_LOGO_B = 'github-mark.svg'
KOFI_LOGO_B = 'kofi_s_logo_nolabel.webp'

# Files in PAYDAY2/Mods/ to ignore
MODSIGNORE = ('base', 'logs', 'saves', 'downloads')

# These tuples are usually meant to be unpacked as arguments using the * prefix
DATA_PROFILE = (0, ProfileRole.type, 'profile') # Used to label an item as a profile
DATA_MOD = (0, ProfileRole.type, 'mod') # Used to label an item as a mod

# Default Disabled Folder
MODS_DISABLED_PATH_DEFAULT: str = os.path.join(ROOT_PATH, DISABLED_MODS)

# Graphics folder path
UI_GRAPHICS_PATH: str = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'graphics')

# Color Themes
DARK = 'dark'
LIGHT = 'light'

# Program Info
PROGRAM_NAME = 'Myth Mod Manager'

VERSION = semantic_version.Version(major=1, minor=7, patch=1)
