
import os
import semantic_version

# Detection if the program is being run through an exe or the script
IS_SCRIPT = os.path.exists(os.path.join(os.path.dirname(__file__), 'main.py'))

# Root Path
ROOT_PATH = os.path.abspath(os.path.join(os.curdir, 'src')) if IS_SCRIPT else os.curdir

# File names
MOD_CONFIG = 'mods.ini'
OPTIONS_CONFIG = 'config.ini'
START_PAYDAY = 'runGame.bat'
DISABLED_MODS = 'disabled-mods'
BACKUP_MODS = 'backup mods'

# Mod Table Object Name
MOD_TABLE_OBJECT = 'mod_table'

# Keys that a mod has
MOD_ENABLED = 'enabled'
MOD_TYPE = 'type'

# Files in PAYDAY2/Mods/ to ignore
MODSIGNORE = ('base', 'logs', 'saves', 'downloads')

# The type of mods
TYPE_MODS = 'mods'
TYPE_MODS_OVERRIDE = 'mods_override'

# Option Sections
OPTIONS_SECTION = 'OPTIONS'

# Keys in OPTIONS_CONFIG
OPTIONS_GAMEPATH = 'game_path'
OPTIONS_DISPATH = 'disabled-mods'

# Default Disabled Folder
MODS_DISABLED_PATH_DEFAULT = os.path.join(os.path.abspath(ROOT_PATH), DISABLED_MODS)

# START_PAYDAY Path
START_PAYDAY_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), START_PAYDAY)

# Program Info
PROGRAM_NAME = 'Myth Mod Manager'
VERSION = semantic_version.Version(major=1, minor=0, patch=0, prerelease=('beta', '2'))