
import os

import semantic_version

# Detection if the program is being run through an exe or the script
IS_SCRIPT = os.path.exists(os.path.join(os.path.dirname(__file__), 'main.py'))

# Root Path
ROOT_PATH = os.path.abspath(os.path.join(os.curdir, 'src')) if IS_SCRIPT else os.curdir

# Icon Path
ICON = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'icon.ico')

# File names
MOD_CONFIG = 'mods.ini'
OPTIONS_CONFIG = 'config.ini'
START_PAYDAY = 'runGame.bat'
DISABLED_MODS = 'disabled-mods'
BACKUP_MODS = 'backup mods'
LOG = 'log.txt'

# Mod Table Object Name
MOD_TABLE_OBJECT = 'mod_table'

# Keys that a mod has
MOD_ENABLED = 'enabled'
MOD_TYPE = 'type'

# Files in PAYDAY2/Mods/ to ignore
MODSIGNORE = ('base', 'logs', 'saves', 'downloads')

# The type of mods
TYPE_ALL = ('mods', 'mods_override', 'maps')
TYPE_MODS = TYPE_ALL[0]
TYPE_MODS_OVERRIDE = TYPE_ALL[1]
TYPE_MAPS = TYPE_ALL[2]

# Option Sections
OPTIONS_SECTION = 'OPTIONS'

# Keys in OPTIONS_CONFIG
OPTIONS_GAMEPATH = 'game_path'
OPTIONS_DISPATH = 'disabled-mods'
OPTIONS_THEME = 'color_theme'

# Default Disabled Folder
MODS_DISABLED_PATH_DEFAULT = os.path.join(os.path.abspath(ROOT_PATH), DISABLED_MODS)

# START_PAYDAY Path
START_PAYDAY_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), START_PAYDAY)

# Color Themes
DARK = 'dark'
LIGHT = 'light'

# Program Info
PROGRAM_NAME = 'Myth Mod Manager'
VERSION = semantic_version.Version(major=1, minor=0, patch=1)