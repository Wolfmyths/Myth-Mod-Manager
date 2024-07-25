import pytest
from pytestqt.qtbot import QtBot

from semantic_version import Version

from src.widgets.QDialog.newUpdateQDialog import updateDetected
from src.constant_vars import VERSION

@pytest.fixture
def create_dialog(qtbot: QtBot) -> updateDetected:
    widget = updateDetected(Version(major=1, minor=5, patch=6), 'release notes')
    qtbot.addWidget(widget)

    yield widget

#TODO: Find a way to test this without the Notice.exec() being called
@pytest.mark.skip
def test_errorRaised(create_dialog: updateDetected) -> None:

    create_dialog.autoUpdate.error.emit('error')

def test_dialog(create_dialog: updateDetected) -> None:
    assert create_dialog.message.text() == f'New update found: 1.5.6\nCurrent Version: {VERSION}\nDo you want to Update?'
    assert create_dialog.changelog.document().toPlainText() == 'release notes'

def test_succeeded(create_dialog: updateDetected) -> None:

    create_dialog.progressBar.show()
    create_dialog.autoUpdate.succeeded.emit()

    assert create_dialog.message.text() == 'Installation Successful!\nClick ok to exit and update Myth Mod Manager'
    assert create_dialog.progressBar.value() == create_dialog.progressBar.maximum()
    assert create_dialog.succeededState
    assert create_dialog.progressBar.isHidden()

def test_cancel(create_dialog: updateDetected) -> None:

    create_dialog.progressBar.show()
    create_dialog.cancel()

    assert create_dialog.message.text() == 'Canceling... (Finishing current step)'
    assert create_dialog.autoUpdate.cancel == True

    create_dialog.autoUpdate.doneCanceling.emit()

    assert create_dialog.result() == 0

def test_updateProgressBar(create_dialog: updateDetected) -> None:

    create_dialog.autoUpdate.setTotalProgress.emit(100)
    assert create_dialog.progressBar.maximum() == 100

    create_dialog.autoUpdate.addTotalProgress.emit(100)
    assert create_dialog.progressBar.maximum() == 200

    create_dialog.autoUpdate.setCurrentProgress.emit(51, 'testing ^_^')
    assert create_dialog.progressBar.value() == 50
    assert create_dialog.message.text() == 'testing ^_^'

def test_downloadStarted(create_dialog: updateDetected) -> None:
    total = 900

    assert create_dialog.downloadState == False

    create_dialog.downloadStarted(101, total)

    assert create_dialog.progressBar.maximum() == 1000
    assert create_dialog.progressBar.value() == 100
    assert create_dialog.lastIterBytes == 101
    assert create_dialog.downloadState
