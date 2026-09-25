from typing import Callable, override
from collections.abc import Generator
import tempfile
import json
import os

from PySide6.QtNetwork import QNetworkReply, QNetworkRequest
from PySide6.QtCore import QByteArray, QDir, QObject, QTimer

import pytest
from pytestqt.qtbot import QtBot

from src.constant_vars import OLD_EXE
from src.api.update import Update
from tests.mock_baseclasses.mock_qnetworkaccessmanager import Mock_QNetworkAccessManagerBase
from tests.mock_baseclasses.mock_qnetworkreply import Mock_QNetworkReplyBase

class Mock_QNetworkReply(Mock_QNetworkReplyBase):

    MOCK_ASSETS_URL_RESULT = {'assets_url' : 'yo_mamma.com'}
    MOCK_DOWNLOAD_ASSETS_RESULT = [{
        'name' : Update.fileName,
        'browser_download_url' : "skibidi toilet pomni sigma"
    }]
    MOCK_DOWNLOAD_UPDATE_RESULT = "Mock file but pretend this is bytes"

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        QTimer.singleShot(1, self, lambda: self.finished.emit(self))
    
    def error(self) -> QNetworkReply.NetworkError:
        return QNetworkReply.NetworkError.NoError
    
    def errorString(self) -> str:
        return "MockErrorString"
    
    def readAll(self) -> QByteArray:   
        match Mock_QNetworkAccessManager.stage:
            case 0:
                byte_dump = json.dumps(Mock_QNetworkReply.MOCK_ASSETS_URL_RESULT).encode()
            case 1:
                byte_dump = json.dumps(Mock_QNetworkReply.MOCK_DOWNLOAD_ASSETS_RESULT).encode()
            case 2:
                byte_dump = bytes(Mock_QNetworkReply.MOCK_DOWNLOAD_UPDATE_RESULT, "utf-8")
            case _:
                byte_dump = bytes()
                assert False
            
        return QByteArray(byte_dump)

class Mock_QNetworkAccessManager(Mock_QNetworkAccessManagerBase):
    stage = -1
    
    @override
    def get(self, _request: QNetworkRequest) -> Mock_QNetworkReply:
        Mock_QNetworkAccessManager.stage += 1
        return Mock_QNetworkReply()

TMP_EXECUTABLE_NAME = "Mock_MMM.exe.txt"

@pytest.fixture
def patch_network_stuff(monkeypatch: pytest.MonkeyPatch) -> Generator[str]:
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_dir_abspath = QDir.toNativeSeparators(QDir.temp().filePath(tmp_dir.name))
    tmp_root = os.path.join(tmp_dir_abspath, "MockRoot")
    os.mkdir(tmp_root)
    tmp_executable_path = os.path.join(tmp_root, TMP_EXECUTABLE_NAME)
    tmp_downloaded_exec_path = os.path.join(tmp_dir_abspath, TMP_EXECUTABLE_NAME)

    for path in (tmp_executable_path, tmp_downloaded_exec_path):
        with open(path, "w") as _f:
            pass

    monkeypatch.setattr("src.api.update.ROOT_PATH", tmp_root)

    yield tmp_dir.name

    tmp_dir.cleanup()

@pytest.fixture
def update(monkeypatch: pytest.MonkeyPatch, patch_network_stuff: str) -> Generator[Update]:  # pyright: ignore[reportUnusedParameter]
    shutil_patch: Callable[[str, str], None] = lambda x, y: None

    monkeypatch.setattr("src.api.update.QNetworkAccessManager", Mock_QNetworkAccessManager)
    monkeypatch.setattr("src.api.update.QNetworkReply", Mock_QNetworkReply)
    monkeypatch.setattr("src.api.update.shutil.unpack_archive", shutil_patch)

    is_destroyed = False

    def on_destroyed() -> None:
        nonlocal is_destroyed
        is_destroyed = True

    update = Update()
    update.destroyed.connect(on_destroyed) # Update deletes itself in most cases
    yield update

    if not is_destroyed:
        update.deleteLater()

def test_update(update: Update, patch_network_stuff: str, qtbot: QtBot) -> None:
    update.exe = TMP_EXECUTABLE_NAME
    update.folder = patch_network_stuff

    with qtbot.waitSignal(update.succeeded, timeout=10):
        update.start()
    
    mockroot_path = os.path.join(update.tmp, patch_network_stuff, "MockRoot")

    assert os.path.exists(os.path.join(mockroot_path, OLD_EXE)) is True
    assert os.path.exists(os.path.join(mockroot_path, TMP_EXECUTABLE_NAME)) is True