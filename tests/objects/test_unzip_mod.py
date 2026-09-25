from collections.abc import Generator
import shutil
import os
import tempfile

import pytest

from pytestqt.qtbot import QtBot

from src.helpers.options_manager import OptionsManager
from src.objects.unzip_mod import UnZipMod
from src.constant_vars import ModType

@pytest.fixture
def tmp_named_file() -> Generator[str]:
    with tempfile.NamedTemporaryFile("w") as tmp_file:
        yield tmp_file.name

@pytest.fixture
def unzipmod(monkeypatch: pytest.MonkeyPatch, create_mod_dirs: str) -> Generator[UnZipMod]:
    def replace_extract_archive(archive: str, outdir: str | None = None) -> str:
        return shutil.move(archive, outdir)  # pyright: ignore[reportArgumentType]

    monkeypatch.setattr(
        OptionsManager, "getGamepath", lambda: create_mod_dirs)
    assert OptionsManager.getGamepath() == create_mod_dirs

    monkeypatch.setattr(
        "src.objects.unzip_mod.patoolib.extract_archive", replace_extract_archive)
    
    unzipmod = UnZipMod()

    yield unzipmod

    unzipmod.deleteLater()


def test_thread(unzipmod: UnZipMod, tmp_named_file: str,
qtbot: QtBot, create_mod_dirs: str, 
createTemp_Config_ini: str, createTemp_Mod_ini: str) -> None:  # pyright: ignore[reportUnusedParameter]

    unzipmod.mods = ((tmp_named_file, ModType.mods), )

    with qtbot.wait_signal(unzipmod.succeeded, timeout=500):
        unzipmod.start()

    assert os.path.exists(os.path.join(create_mod_dirs, 'mods', os.path.basename(tmp_named_file))) is True
