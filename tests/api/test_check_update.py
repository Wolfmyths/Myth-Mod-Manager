from collections.abc import Generator
import json
from typing import override

from PySide6.QtCore import QByteArray, QObject, QTimer, QVersionNumber

from PySide6.QtNetwork import QNetworkReply, QNetworkRequest
import pytest
from pytestqt.qtbot import QtBot

from src.api.check_update import CheckUpdate
from tests.mock_baseclasses.mock_qnetworkreply import Mock_QNetworkReplyBase
from tests.mock_baseclasses.mock_qnetworkaccessmanager import Mock_QNetworkAccessManagerBase

class Mock_QNetworkReply(Mock_QNetworkReplyBase):
    MOCK_REPLY_RESULT = {
        'tag_name' : '1.0.3',
        'body'     : 'body text'}

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        QTimer.singleShot(1, lambda: self.finished.emit(self))
    
    def error(self) -> QNetworkReply.NetworkError:
        return self.NetworkError.NoError

    def readAll(self) -> QByteArray:
        return QByteArray(
            json.dumps(Mock_QNetworkReply.MOCK_REPLY_RESULT).encode())

class Mock_QNetworkReplyError(Mock_QNetworkReplyBase):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        QTimer.singleShot(1, self, lambda: self._emit_error_occurred())
    
    def error(self) -> QNetworkReply.NetworkError:
        return self.NetworkError.UnknownNetworkError

    def _emit_error_occurred(self) -> None:
        self.errorOccurred.emit(self.NetworkError.UnknownNetworkError)
        self.finished.emit(self)

class Mock_QNetworkAccessManager(Mock_QNetworkAccessManagerBase):
    @override
    def get(self, _request: QNetworkRequest) -> Mock_QNetworkReply:
        return Mock_QNetworkReply()

class Mock_QNetworkAccessManagerError(Mock_QNetworkAccessManagerBase):
    @override
    def get(self, _request: QNetworkRequest) -> Mock_QNetworkReplyError:
        return Mock_QNetworkReplyError()

@pytest.fixture
def checkupdate() -> Generator[CheckUpdate]:
    checkupdate = CheckUpdate()
    yield checkupdate
    checkupdate.deleteLater()

def test_CheckUpdate(checkupdate: CheckUpdate, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.api.check_update.QNetworkAccessManager", Mock_QNetworkAccessManager)
    monkeypatch.setattr("src.api.check_update.VERSION", QVersionNumber(1,0,0))

    with qtbot.wait_signal(checkupdate.updateDetected, timeout=10):
        checkupdate.start()

    monkeypatch.setattr("src.api.check_update.VERSION", QVersionNumber(1,0,4))

    with qtbot.wait_signal(checkupdate.upToDate, timeout=10):
        checkupdate.start()

def test_CheckUpdateError(checkupdate: CheckUpdate, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.api.check_update.QNetworkAccessManager", Mock_QNetworkAccessManagerError)
    monkeypatch.setattr("src.api.check_update.QNetworkReply", Mock_QNetworkReplyError)

    with qtbot.waitSignal(checkupdate.error, timeout=10):
        checkupdate.start()
