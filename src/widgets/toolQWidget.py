import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QSize

from src.toolsData import ToolJSON
from src.widgets.toolDisplayQWidget import ExternalTool
from src.widgets.QDialog.announcementQDialog import Notice

from src.constant_vars import TOOLS_JSON

class ExternalToolDisplay(qtw.QListWidget):
    def __init__(self, json = TOOLS_JSON) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.json = ToolJSON(json)

        self.setWrapping(True)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setMovement(self.Movement.Static)
        self.setFlow(self.Flow.LeftToRight)
        self.setSpacing(4)

        self.addTool(*self.json.getShortcuts(), save=False)

    def addTool(self, *url: str, save: bool = True) -> None:

        dupes: list[str] = []

        if save:
            dupes = self.json.newTool(*url)

        for s in url:

            if s in dupes: continue

            item = qtw.QListWidgetItem(s)
            item.setFlags(qt.ItemFlag.ItemIsEnabled | qt.ItemFlag.ItemNeverHasChildren)
            self.addItem(item)

            frame = ExternalTool(s)
            frame.deleted.connect(lambda: self.deleteItem(item, s))
            frame.nameChanged.connect(lambda x: self.changeName(item, x))
            item.setSizeHint(QSize(245, 245))

            self.setItemWidget(item, frame)
        
        if dupes:
            notice = Notice(f'Shortcuts were not added because they already exist: {", ".join(dupes)}',
                            'Duplicate shortcuts found')
            notice.exec()
    
    def deleteItem(self, item: qtw.QListWidgetItem, url: str) -> None:
        self.takeItem(self.row(item))
        self.json.removeTool(url)

    def changeName(self, item: qtw.QListWidgetItem, newUrl: str) -> None:
        oldURL = item.text()
        item.setText(newUrl)
        self.json.changeTool(oldURL, newUrl)
