from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import sys

label = ""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgba(255,255,255,0.5);")
        self.setWindowTitle("Color")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
        label = QLabel("\n 0 / 15 刷  0 / 7 關", self)
        # label.setStyleSheet("background-color: rgba(255,255,255,0);")
        label.setStyleSheet("background-color: gray;")
        label.setFont(QFont('Microsoft JhengHei', 18, QFont.Bold))
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

    def setTextToLabel(str):
        label.setText(str)
