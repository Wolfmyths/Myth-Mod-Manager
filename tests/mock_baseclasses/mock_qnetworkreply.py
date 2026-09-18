from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QNetworkReply

class Mock_QNetworkReplyBase(QObject):
    class NetworkError:
        NoError = QNetworkReply.NetworkError.NoError
        UnknownNetworkError = QNetworkReply.NetworkError.UnknownNetworkError
    
    finished = Signal(QObject) # Mock_QNetworkReply
    errorOccurred = Signal(QNetworkReply.NetworkError)
    downloadProgress = Signal(int, int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        