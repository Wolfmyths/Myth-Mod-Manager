import PySide6.QtWidgets as qtw

class ModContextMenu(qtw.QMenu):
    def __init__(self, parent: qtw.QListWidget) -> None:
        super().__init__()
