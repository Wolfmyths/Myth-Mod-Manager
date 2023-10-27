import os
import shutil

import pytest

from PySide6.QtCore import QUrl

from src.threaded.unZipMod import UnZipMod
from src.constant_vars import ModType
from src.getPath import Pathing
from src.save import OptionsManager, Save

#TODO: Make a QUrl that works. Calling QUrl.toLocalFile() returns '' for some reason
@pytest.mark.skip
def test_thread(create_mod_dirs: str, createTemp_Config_ini: str) -> None:
    parser = OptionsManager(createTemp_Config_ini)
    parser.setGamepath(create_mod_dirs)
    parser.writeData()

    zip_path = os.path.join(create_mod_dirs, 'zip')
    os.mkdir(zip_path)
    shutil.make_archive(zip_path, 'zip')

    thread = UnZipMod()
    thread.optionsManager = parser
    thread.saveManager = Save(create_mod_dirs)

    thread.p = Pathing(createTemp_Config_ini)

    qurl = QUrl(os.path.join(create_mod_dirs, 'zip.zip'))

    thread.unZipMod((qurl, ModType.mods))

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'zip'))
