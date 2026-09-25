from PySide6.QtCore import QObject
from PySide6.QtNetwork import QNetworkRequest

from tests.mock_baseclasses.mock_qnetworkreply import Mock_QNetworkReplyBase

class Mock_QNetworkAccessManagerBase:
    def __init__(self, _parent: QObject | None = None) -> None:
        ...

    def get(self, _request: QNetworkRequest) -> Mock_QNetworkReplyBase:
        return Mock_QNetworkReplyBase()