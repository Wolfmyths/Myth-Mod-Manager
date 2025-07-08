import logging

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt, QSize, QCoreApplication as qapp, Slot

from src.toolsData import ToolJSON
from src.widgets.toolDisplayQWidget import ExternalTool
from src.widgets.QDialog.announcementQDialog import Notice

class ExternalToolDisplay(qtw.QListWidget):
    external_tools: list[ExternalTool] = []
    def __init__(self) -> None:
        super().__init__()
        logging.getLogger(__name__)

        self.setWrapping(True)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setMovement(self.Movement.Static)
        self.setFlow(self.Flow.LeftToRight)
        self.setSpacing(4)

        self.addTool(*ToolJSON.getShortcuts(), save=False)

    def addTool(self, *url: str, save: bool = True) -> None:

        dupes: list[str] = []

        if save:
            dupes = ToolJSON.newTool(*url)
            ToolJSON.save()

        for s in url:

            if s in dupes:
                continue

            item = qtw.QListWidgetItem(s)
            item.setFlags(qt.ItemFlag.ItemIsEnabled | qt.ItemFlag.ItemNeverHasChildren)
            self.addItem(item)

            frame = ExternalTool(s)
            frame.deleted.connect(self.deleteItem)
            frame.nameChanged.connect(self.changeName)
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
        
        try:
            item: qtw.QListWidgetItem = self.findItems(url, qt.MatchFlag.MatchExactly)[0]
        except IndexError as e:
            logging.error(
                'ExternalToolDisplay.deleteItem(): Looked for %s and could not find it\n%s',
                url, e
            )
            return

        index: int = self.row(item)
        self.external_tools.pop(index)
        self.takeItem(index)

        ToolJSON.removeTool(url)
        ToolJSON.save()

    @Slot(str, str)
    def changeName(self, newUrl: str, oldUrl: str) -> None:
        
        try:
            item: qtw.QListWidgetItem = self.findItems(oldUrl, qt.MatchFlag.MatchExactly)[0]
        except IndexError as e:
            logging.error(
                'ExternalToolDisplay.changeName(): Looked for %s and could not find it\n%s',
                oldUrl, e
            )
            return

        item.setText(newUrl)

        ToolJSON.changeTool(oldUrl, newUrl)
        ToolJSON.save()
