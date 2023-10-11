from PySide6.QtCore import QThread, Signal

class Thread(QThread):
    '''Base Class for threading inheriting PySide's QThread'''

    setTotalProgress = Signal(int)

    addTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    doneCanceling = Signal()

    error = Signal(str)

    cancel = False
