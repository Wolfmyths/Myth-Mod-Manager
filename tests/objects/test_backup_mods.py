from collections.abc import Generator
from typing import Callable
import os
import shutil

import pytest
from pytestqt.qtbot import QtBot

from src.objects.backup_mods import BackupMods

mock_backupmods_folder_name = "backedupmods"

@pytest.fixture
def backupmods(monkeypatch: pytest.MonkeyPatch, create_mod_dirs: str) -> Generator[BackupMods]:
    replace_getdispath: Callable[[], str] = lambda: os.path.join(create_mod_dirs, "disabledMods")
    replace_mods: Callable[[], str] = lambda: os.path.join(create_mod_dirs, "mods")
    replace_mod_overrides: Callable[[], str] = lambda: os.path.join(create_mod_dirs, "assets", "mod_overrides")
    replace_maps: Callable[[], str] = lambda: os.path.join(create_mod_dirs, "Maps")
    monkeypatch.setattr("src.objects.backup_mods.OptionsManager.getDispath", replace_getdispath)
    monkeypatch.setattr("src.objects.backup_mods.Pathing.mods", replace_mods)
    monkeypatch.setattr("src.objects.backup_mods.Pathing.mod_overrides", replace_mod_overrides)
    monkeypatch.setattr("src.objects.backup_mods.Pathing.maps", replace_maps)
    monkeypatch.setattr("src.objects.backup_mods.BACKUP_MODS",
        os.path.join(create_mod_dirs, mock_backupmods_folder_name))

    backupmods = BackupMods()
    backupmods.error.connect(print)

    yield backupmods

    backupmods.deleteLater()

def test_backupmods(qtbot: QtBot, backupmods: BackupMods, create_mod_dirs: str, createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:  # pyright: ignore[reportUnusedParameter]
    
    base_dir = os.path.join(create_mod_dirs, mock_backupmods_folder_name)
    os.mkdir(base_dir)

    backupmods.bundledFilePath = base_dir

    with qtbot.wait_signal(backupmods.succeeded, timeout=500):
        backupmods.start()

    archive = f"{base_dir}.zip"

    #print("Dir of", create_mod_dirs, os.listdir(create_mod_dirs))
    #print("Path to archive", archive)
    assert os.path.exists(archive) is True

    shutil.unpack_archive(archive, base_dir, format="zip")

    #print("Dir of", create_mod_dirs, "after unpack:", os.listdir(create_mod_dirs))

    bundleFilePathFiles = os.listdir(base_dir)
    modFiles = os.listdir(os.path.join(base_dir, 'mods'))
    modoverrideFiles = os.listdir(os.path.join(base_dir, 'assets', 'mod_overrides'))
    mapFiles = os.listdir(os.path.join(base_dir, 'Maps'))

    #print(base_dir, modFiles, modoverrideFiles, mapFiles)

    assert set(bundleFilePathFiles) == set(['mods', 'assets', 'Maps'])
    assert modFiles == ['make game easy mod']
    assert modoverrideFiles == ['best mod ever']
    assert mapFiles == ['super fun mod']
