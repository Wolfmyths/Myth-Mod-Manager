import os

from PySide6.QtCore import QMutex

from src.objects.delete_mod import DeleteMod


def test_thread(create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:
    mutex = QMutex()
    worker = DeleteMod('make game easy mod')
    worker.mutex = mutex

    worker.start()

    assert os.path.isdir(os.path.join(create_mod_dirs, 'mods', 'make game easy mod')) is False

    worker.deleteLater()
