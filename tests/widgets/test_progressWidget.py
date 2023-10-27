import pytest
from pytestqt.qtbot import QtBot

from src.widgets.progressWidget import ProgressWidget
from src.threaded.file_mover import FileMover

@pytest.fixture(scope='function')
def create_progressWidget(qtbot: QtBot) -> tuple[FileMover, ProgressWidget, QtBot]:
    obj = FileMover()
    widget = ProgressWidget(obj)

    qtbot.addWidget(widget)

    return obj, widget, qtbot

def test_errorRaised(create_progressWidget: tuple[FileMover, ProgressWidget, QtBot]) -> None:

    create_progressWidget[0].error.emit('error')

    assert create_progressWidget[1].warningLabel.text() == 'error'

def test_succeeded(create_progressWidget: tuple[FileMover, ProgressWidget, QtBot]) -> None:

    create_progressWidget[0].succeeded.emit()

    assert create_progressWidget[1].warningLabel.text() == 'Done!'
    assert create_progressWidget[1].progressBar.value() == create_progressWidget[1].progressBar.maximum()
    assert create_progressWidget[1].result() == 1

def test_cancel(create_progressWidget: tuple[FileMover, ProgressWidget, QtBot]) -> None:

    create_progressWidget[1].cancel()

    assert create_progressWidget[1].warningLabel.text() == 'Canceling... (Finishing current step)'
    assert create_progressWidget[0].cancel

    create_progressWidget[1].cancel()

    assert create_progressWidget[1].result() == 0

    create_progressWidget[0].doneCanceling.emit()

    assert create_progressWidget[1].result() == 0

def test_updateProgressBar(create_progressWidget: tuple[FileMover, ProgressWidget, QtBot]) -> None:

    create_progressWidget[0].setTotalProgress.emit(100)
    assert create_progressWidget[1].progressBar.maximum() == 100

    create_progressWidget[0].addTotalProgress.emit(100)
    assert create_progressWidget[1].progressBar.maximum() == 200

    create_progressWidget[0].setCurrentProgress.emit(51, 'testing ^_^')
    assert create_progressWidget[1].progressBar.value() == 50
    assert create_progressWidget[1].warningLabel.text() == 'testing ^_^'