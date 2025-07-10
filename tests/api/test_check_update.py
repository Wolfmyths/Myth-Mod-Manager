from PySide6.QtNetwork import QNetworkReply

from src.api.check_update import CheckUpdate

#TODO: Test this better with mocking
def test_CheckUpdate() -> None:
    obj = CheckUpdate()

    assert obj.reply.error() == QNetworkReply.NetworkError.NoError
