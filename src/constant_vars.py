
import os

# File names
MOD_CONFIG = 'mods.ini'
OPTIONS_CONFIG = 'config.ini'
START_PAYDAY = 'runGame.bat'

# Mod List Object Names
MOD_OVERRIDE_LIST_OBJECT = 'mod_list_override'
MOD_LIST_OBJECT = 'mod_list'

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

# Keys in a section
OPTIONS_GAMEPATH = 'game_path'
OPTIONS_DISPATH = 'disabled-mods'

# Default Disabled Folder
MODS_DISABLED_PATH_DEFAULT = os.path.join(os.path.abspath(os.curdir), 'src', OPTIONS_DISPATH)

# START_PAYDAY Path
START_PAYDAY_PATH = os.path.join(os.path.abspath(os.curdir), 'src', START_PAYDAY)

# Program Version Number
VERSION = '1.0'