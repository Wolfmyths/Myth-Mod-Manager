import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QSize, QCoreApplication as qapp, Slot

from src.toolsData import ToolJSON
from src.widgets.toolDisplayQWidget import ExternalTool
from src.widgets.QDialog.announcementQDialog import Notice

from src.constant_vars import TOOLS_JSON

class ExternalToolDisplay(qtw.QListWidget):
    external_tools: list[ExternalTool] = []
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
            self.json.saveJSON()

        for s in url:

            if s in dupes: continue

            item = qtw.QListWidgetItem(s)
            item.setFlags(qt.ItemFlag.ItemIsEnabled | qt.ItemFlag.ItemNeverHasChildren)
            self.addItem(item)

            frame = ExternalTool(s)
            frame.deleted.connect(lambda x: self.deleteItem(x))
            frame.nameChanged.connect(lambda x, y: self.changeName(x, y))
            item.setSizeHint(QSize(245, 245))

            self.setItemWidget(item, frame)
            self.external_tools.append(frame)
        
        if dupes:
            notice = Notice(
                qapp.translate('ExternalToolDisplay', 'Shortcuts were not added because they already exist:') + f' {", ".join(dupes)}',
                qapp.translate('ExternalToolDisplay', 'Duplicate shortcuts found')
            )
            notice.exec()
    
    @Slot(str)
    def deleteItem(self, url: str) -> None:
        item = self.findItems(url, qt.MatchFlag.MatchExactly)
        if item:
            item = item[0]
        else:
            logging.error('ExternalToolDisplay.deleteItem(): Looked for %s and could not find it', url)
            return

        index = self.row(item)
        self.external_tools.pop(index)
        self.takeItem(index)

        self.json.removeTool(url)
        self.json.saveJSON()

    @Slot(str, str)
    def changeName(self, newUrl: str, oldUrl: str) -> None:
        item = self.findItems(oldUrl, qt.MatchFlag.MatchExactly)
        if item:
            item = item[0]
        else:
            logging.error('ExternalToolDisplay.changeName(): Looked for %s and could not find it', oldUrl)
            return

        item.setText(newUrl)

        self.json.changeTool(oldUrl, newUrl)
        self.json.saveJSON()
