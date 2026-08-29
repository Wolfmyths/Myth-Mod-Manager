import pytest
from collections.abc import Generator

from pytestqt.qtbot import QtBot

from PySide6.QtCore import QVersionNumber

from src.widgets.qdialog.update_detected import UpdateDetected
from src.constant_vars import VERSION

@pytest.fixture(scope='function')
def create_dialog(qtbot: QtBot) -> Generator[UpdateDetected]:
    widget = UpdateDetected(QVersionNumber(1, 5, 6).toString(), 'release notes')
    qtbot.addWidget(widget)

    yield widget

#TODO: Find a way to test this without the Notice.exec() being called
@pytest.mark.skip
def test_errorRaised(create_dialog: UpdateDetected) -> None:

    create_dialog.autoUpdate.error.emit('error')

def test_dialog(create_dialog: UpdateDetected) -> None:
    assert create_dialog.message.text() == f'New update found: 1.5.6\nCurrent Version: {VERSION.toString()}\nDo you want to Update?'
    assert create_dialog.changelog.document().toPlainText() == 'release notes'

def test_succeeded(create_dialog: UpdateDetected) -> None:

    create_dialog.progressBar.show()
    create_dialog.autoUpdate.succeeded.emit()

    assert create_dialog.message.text() == 'Installation Successful!\nClick ok to exit and update Myth Mod Manager'
    assert create_dialog.progressBar.value() == create_dialog.progressBar.maximum()
    assert create_dialog.succeededState
    assert create_dialog.progressBar.isHidden()

def test_cancel(create_dialog: UpdateDetected) -> None:

    create_dialog.progressBar.show()
    create_dialog.cancel()

    assert create_dialog.message.text() == 'Canceling... (Finishing current step)'
    assert create_dialog.autoUpdate.cancel is True

    create_dialog.autoUpdate.doneCanceling.emit()

    assert create_dialog.result() == 0

def test_updateProgressBar(create_dialog: UpdateDetected) -> None:

    create_dialog.autoUpdate.setTotalProgress.emit(100)
    assert create_dialog.progressBar.maximum() == 100

    create_dialog.autoUpdate.addTotalProgress.emit(100)
    assert create_dialog.progressBar.maximum() == 200

    create_dialog.autoUpdate.setCurrentProgress.emit(51, 'testing ^_^')
    assert create_dialog.progressBar.value() == 50
    assert create_dialog.message.text() == 'testing ^_^'

def test_downloadStarted(create_dialog: UpdateDetected) -> None:
    total = 900

    assert create_dialog.downloadState is False

    create_dialog.onDownloadProgress(101, total)

    assert create_dialog.progressBar.maximum() == 900
    assert create_dialog.progressBar.value() == 101
    assert create_dialog.downloadState is True
