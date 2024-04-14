from __future__ import annotations
from typing import TYPE_CHECKING, Callable

import PySide6.QtWidgets as qtw
from PySide6.QtCore import Qt as qt

if TYPE_CHECKING:
    import PySide6.QtGui as qtg

class ModContextMenu(qtw.QMenu):
    '''Base class for QMenu Objects'''

    lastClicked: qt.MouseButton = None
    lastReleased: qt.MouseButton = None
    def __init__(self, parent: qtw.QWidget | None = None) -> None:
        super().__init__(parent)
    
    def wasLastClickLMB(self) -> bool:
        '''For ignoring right click inputs when the menu is open'''
        return self.lastClicked == qt.MouseButton.LeftButton and self.lastReleased == qt.MouseButton.LeftButton
    
    def callFunc(self, func: Callable[[], None]) -> None:
        '''
        Calls a function that as long as the user
        did not right-click to trigger this function
        '''

        if self.wasLastClickLMB():
            func()

# EVENT OVERRIDES
    def mousePressEvent(self, arg__1: qtg.QMouseEvent) -> None:
        self.lastClicked = arg__1.button()
        return super().mousePressEvent(arg__1)
    
    def mouseReleaseEvent(self, arg__1: qtg.QMouseEvent) -> None:
        self.lastReleased = arg__1.button()
        return super().mouseReleaseEvent(arg__1)
