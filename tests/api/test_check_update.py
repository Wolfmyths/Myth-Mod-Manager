from pytestqt.qtbot import QtBot

from src.api.check_update import CheckUpdate

# TODO: Make test better possibly with mock functions
def test_CheckUpdate(qtbot: QtBot) -> None:
    obj = CheckUpdate()

    with qtbot.wait_signal(obj.done, raising=True):
        obj.start()

    obj.deleteLater()
