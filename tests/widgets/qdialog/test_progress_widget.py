import pytest
from collections.abc import Generator

from src.widgets.qdialog.progress_widget import ProgressWidget
from src.objects.worker import Worker

@pytest.fixture(scope='function')
def create_progressWidget(createTemp_Config_ini: str, createTemp_Mod_ini: str) -> Generator[ProgressWidget]:  # pyright: ignore[reportUnusedParameter]
    worker = Worker()
    widget = ProgressWidget(worker)

    yield widget

    worker.deleteLater()
    widget.deleteLater()

def test_errorRaised(create_progressWidget: ProgressWidget) -> None:
    create_progressWidget.errorRaised('error')

    assert create_progressWidget.infoLabel.text() == 'error\nExit to continue'

def test_succeeded(create_progressWidget: ProgressWidget) -> None:
    create_progressWidget.succeeded()

    assert create_progressWidget.infoLabel.text() == 'Done!'
    assert create_progressWidget.progressBar.value() == create_progressWidget.progressBar.maximum()
    assert create_progressWidget.result() == 1

def test_cancel(create_progressWidget: ProgressWidget) -> None:

    create_progressWidget.cancel()

    assert create_progressWidget.infoLabel.text() == 'Canceled'
    assert create_progressWidget.mode.cancel

    create_progressWidget.cancel()

    assert create_progressWidget.result() == 0

def test_updateProgressBar(create_progressWidget: ProgressWidget) -> None:

    create_progressWidget.updateProgressBar(51, 'testing ^_^')
    assert create_progressWidget.progressBar.value() == 50
    assert create_progressWidget.infoLabel.text() == 'testing ^_^'