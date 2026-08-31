from typing import cast

from PySide6.QtNetwork import QNetworkReply

from src.api.check_update import CheckUpdate

#TODO: Test this better with mocking
def test_CheckUpdate() -> None:
    obj = CheckUpdate()
    obj.start()

    assert cast(QNetworkReply, obj.sender()).error() == QNetworkReply.NetworkError.NoError

    obj.deleteLater()
