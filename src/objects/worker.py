import logging
import shutil

from PySide6.QtCore import QObject, Signal, QMutex, QMutexLocker, QFileInfo, QCoreApplication as qapp

class Worker(QObject):
    setTotalProgress = Signal(int)

    addTotalProgress = Signal(int)

    setCurrentProgress = Signal(int, str)

    succeeded = Signal()

    doneCanceling = Signal()

    error = Signal(str)

    cancel = False

    mutex: QMutex = QMutex() # Should be set externally by the ProgressWidget class

    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

    def start(self) -> None:
        ...

    def onCancel(self) -> None:
        ...

    def rest(self) -> None:
        '''
        Emits signals too fast even with signal blockers so we need this until we can find a better way
        '''
        self.thread().msleep(1)

    def cancelCheck(self) -> None:
        with QMutexLocker(self.mutex):
            if not self.cancel:
                return
        
        logging.info('%s was canceled', self.__class__)
        self.onCancel()
        self.doneCanceling.emit()

    def move(self, src: str, dest: str) -> None:
        '''`shutil.move()` with some extra exception handling'''

        dest_file_info = QFileInfo(dest)
        src_file_info = QFileInfo(src)

        # Will try to move the file, if there is an exception, fix the issue and try again
        try:

            if not QFileInfo(dest_file_info.absolutePath()).exists():
                raise FileNotFoundError(f"File's destination does not exist\n{dest_file_info.absolutePath()}")

            # Overwrite mod
            if dest_file_info.exists():
                shutil.rmtree(dest)
            
            if not src_file_info.exists():
                raise FileNotFoundError(f"File to be moved does not exist\n{src_file_info.absoluteFilePath()}")

            shutil.move(src, dest)
            logging.info('Moved file %s to destination %s', src, dest)

        except Exception as e:

            # If shutil.move made a partial dir of the mod delete it
            if dest_file_info.exists():
                shutil.rmtree(dest)
            
            logging.warning('An error was raised in shutil:\n%s', e)
            self.error.emit(f"{qapp.translate("Worker", "Error")}: {e}")
        
