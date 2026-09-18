from typing import override

from PySide6.QtCore import QByteArray, QObject, QTimer

from PySide6.QtNetwork import QNetworkReply, QNetworkRequest
import pytest
from pytestqt.qtbot import QtBot

from src.api.check_mod_update import CheckModUpdate
from tests.mock_baseclasses.mock_qnetworkreply import Mock_QNetworkReplyBase
from tests.mock_baseclasses.mock_qnetworkaccessmanager import Mock_QNetworkAccessManagerBase

class Mock_QNetworkReply(Mock_QNetworkReplyBase):
    MOCK_REPLY_RESULT = '1.0.2'

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        QTimer.singleShot(1, lambda: self.finished.emit(self))
    
    def error(self) -> QNetworkReply.NetworkError:
        return self.NetworkError.NoError

    def readAll(self) -> QByteArray:
        return QByteArray(bytes(Mock_QNetworkReply.MOCK_REPLY_RESULT, "utf-8"))

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

def test_CheckUpdate(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.api.check_mod_update.QNetworkAccessManager", Mock_QNetworkAccessManager)
    monkeypatch.setattr("src.api.check_mod_update.QNetworkReply", Mock_QNetworkReply)

    obj = CheckModUpdate("", "1.0.0")

    obj.done.connect(lambda: print("Done"))
    obj.error.connect(lambda: print("Error"))
    obj.upToDate.connect(lambda: print("upToDate"))

    with qtbot.wait_signal(obj.updateDetected, timeout=10):
        obj.start()

    obj.deleteLater()

    obj = CheckModUpdate("", "1.0.3")

    with qtbot.wait_signal(obj.upToDate, timeout=10):
        obj.start()

    obj.deleteLater()

def test_CheckUpdateError(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("src.api.check_mod_update.QNetworkAccessManager", Mock_QNetworkAccessManagerError)
    monkeypatch.setattr("src.api.check_mod_update.QNetworkReply", Mock_QNetworkReplyError)

    obj = CheckModUpdate("", "1.0.0")

    with qtbot.waitSignal(obj.error, timeout=10):
        obj.start()
    
    obj.deleteLater()
