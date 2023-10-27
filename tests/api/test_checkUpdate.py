from PySide6.QtNetwork import QNetworkReply

from pytestqt.qtbot import QtBot

from src.api.checkUpdate import checkUpdate

#TODO: Test this better
def test_checkUpdate(qtbot: QtBot) -> None:
    obj = checkUpdate()

    with qtbot.wait_signal(obj.reply.finished, timeout=10000):
        assert obj.reply.error() == QNetworkReply.NetworkError.NoError
