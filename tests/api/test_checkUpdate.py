from PySide6.QtNetwork import QNetworkReply

from src.api.checkUpdate import checkUpdate

#TODO: Test this better with mocking
def test_checkUpdate() -> None:
    obj = checkUpdate()

    assert obj.reply.error() == QNetworkReply.NetworkError.NoError
