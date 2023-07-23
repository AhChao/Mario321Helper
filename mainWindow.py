from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from outlineLabel import OutlinedLabel
import sys
import configparser


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgba(255,255,255,0.5);")
        self.setWindowTitle("Color")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
        label = OutlinedLabel("0 / 15 刷  0 / 7 關", self)
        # label = QLabel(" 0 / 15 刷\n  0 / 7 關", self)
        config = configparser.ConfigParser()
        config.read(r'config.ini', encoding="utf8")
        fontSize = config.get('DisplayConfig', 'fontSize')
        labelStyle = "background-color: rgba(255,255,255,0);\
                    font-family : Microsoft JhengHei;\
                    font-size: "+str(fontSize)+"pt;\
                    font-weight: bold;"
        label.setStyleSheet(labelStyle)
        label.adjustSize()

        self.label = label
        self.show()

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = e.globalPos() - self.previous_pos
        self.move(self.x() + delta.x(), self.y()+delta.y())
        self.previous_pos = e.globalPos()
        self._drag_active = True

    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self._drag_active = False

    def setTextToLabel(self, displayStr):
        self.label.setText(displayStr)
        self.label.adjustSize()
        self.resize(1920, 500)
