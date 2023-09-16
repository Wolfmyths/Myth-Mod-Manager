
import logging

from constant_vars import LIGHT, DARK

class StyleManager():

    darkStyle = ('#0B2447', '#19376D', '#576CBC', '#A5D7E8')

    lightStyle = ('#E7F6F2', '#A5C9CA', '#395B64', '#2C3333')

    style = '''
            QWidget {{
                background-color: {0};
                border-color: {2};
                color: {3};
                font-size: 15px;
                font-family: Bahnschrift;
            }}

            QMenu::item:selected {{
                background: {2};
                color: {1};
            }}

            QLineEdit {{
                border: 2px solid {2};
                border-radius: 10px;
                background: {1};
            }}

            QPushButton {{
                border: 2px solid {2};
                border-radius: 8px;
                background: {1};
                padding: 3px;
            }}

            QPushButton:pressed, QPushButton::checked {{
                border-color: {1};
                background: {2};
                color: {1};
            }}

            QTableView {{
                selection-background-color: {2};
                border: none;
            }}

            QTableView::item {{
                border-color: {1};
                padding: 5px;
            }}

            QHeaderView::section {{
                background-color: {1};
            }}

            QTabBar::tab {{
                background: {1};
                border: 5px solid {1};
                margin-top: 5px;
                margin-right: 5px;
                margin-left: 5px;
            }}

            QTabBar::tab:selected, QTabBar::tab:hover {{
                border-color: {0};
                background: {0};
            }}

            QTabWidget::pane {{
                border-top: 3px solid {2};
            }}

            QTreeView {{
                selection-background-color: {3};
                border: none;
            }}

            QTreeView::item {{
                border-color: {1};
                padding: 5px;
            }}

            QTreeView::item:selected {{
                background: {2};
            }}

            QTreeView::branch {{
            }}

            QListView {{
                selection-background-color: {2};
                border: none;
            }}

            QListView::item {{
                border-color: {1};
                padding: 5px;
            }}

            QListView::item:selected {{
                background: {2};
            }}

            QAbstractItemView {{
                outline: 0;
            }}

            QScrollArea {{
                border: None;
            }}

            QScrollBar:vertical {{
                border: none;
                background-color: {0};
                width: 14px;
                margin: 15px 0 15px 0;
                border-radius: 0px;
                
            }}

            QScrollBar::handle:vertical {{
                background-color: {2};
                min-height: 30px;
                border-radius: 7px;
            }}

            QScrollBar::handle:vertical:hover {{
                background-color: {2};
            }}

            QScrollBar::handle:vertical:pressed {{
                background-color: {3};
                min-height: 30px;
                border-radius: 7px;
            }}

            QScrollBar::sub-line:vertical {{
                border: none;
                background-color: {1};
                height: 15px;
                border-top-left-radius: 7px;
                border-top-right-radius: 7px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}

            QScrollBar::add-line:vertical {{
                border: none;
                background-color: {1};
                height: 15px;
                border-bottom-left-radius: 7px;
                border-bottom-right-radius: 7px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }}

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                background: none;
            }}

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}

            QProgressBar {{
                border: 2px solid {1};
                border-radius: 5px;
                text-align: center;
            }}
            
            QProgressBar::chunk {{
                background-color: {2};
                border-radius: 5px;
            }}

            QGroupBox {{
                border: 15px solid {0};
            }}
            '''

    def __init__(self) -> None:
        logging.getLogger(__name__)

    def getDarkStyle(self) -> str:
        return self.style.format(*self.darkStyle)

    def getLightStyle(self) -> str:
        return self.style.format(*self.lightStyle)

    def getStyleSheet(self, theme: str) -> str:

        try:

            themeDict = {LIGHT : self.getLightStyle, DARK : self.getDarkStyle}

        except KeyError:

            logging.error('This color theme is not valid: %s', theme)

            return

        return themeDict[theme]()