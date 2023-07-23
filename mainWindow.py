from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from outlineLabel import OutlinedLabel
from picButton import PicButton
import sys
import configparser
from videoReader import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: rgba(255,255,255,0.5);")
        self.setWindowTitle("Mario321Helper")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)
        label = OutlinedLabel("0 / 15 刷  0 / 7 關", self)
        # label = QLabel(" 0 / 15 刷\n  0 / 7 關", self)
        config = configparser.ConfigParser()
        config.read(r'config.ini', encoding="utf8")
        fontSize = int(config.get('DisplayConfig', 'fontSize'))
        labelStyle = "background-color: rgba(255,255,255,0);\
                    font-family : Microsoft JhengHei;\
                    font-size: "+str(fontSize)+"pt;\
                    font-weight: bold;"
        label.setStyleSheet(labelStyle)
        label.adjustSize()

        self.label = label

        # init buttons
        if config.get('DisplayConfig', 'displayModifyButton') == "True":
            btnSize = fontSize
            btnBaseLine = fontSize + 45
            refreshAddBtn = PicButton(QPixmap('./imgs/addBtn.png'), self)
            refreshAddBtn.resize(btnSize, btnSize)
            refreshAddBtn.move(fontSize*6, btnBaseLine)
            refreshAddBtn.clicked.connect(
                lambda: operateOnCurrentRefreshCount(1))
            refreshAddBtn.setObjectName("refreshAddBtn")

            refreshMinusBtn = PicButton(
                QPixmap('./imgs/subtractBtn.png'), self)
            refreshMinusBtn.resize(btnSize, btnSize)
            refreshMinusBtn.move(fontSize*7.5, btnBaseLine)
            refreshMinusBtn.clicked.connect(
                lambda: operateOnCurrentRefreshCount(-1))
            refreshMinusBtn.setObjectName("refreshMinusBtn")

            courseClearAddBtn = PicButton(QPixmap('./imgs/addBtn.png'), self)
            courseClearAddBtn.resize(btnSize, btnSize)
            courseClearAddBtn.move(fontSize*14, btnBaseLine)
            courseClearAddBtn.clicked.connect(
                lambda: operateOnCurrentStageCount(1))
            courseClearAddBtn.setObjectName("courseClearAddBtn")

            courseClearMinusBtn = PicButton(
                QPixmap('./imgs/subtractBtn.png'), self)
            courseClearMinusBtn.resize(btnSize, btnSize)
            courseClearMinusBtn.move(fontSize*15.5, btnBaseLine)
            courseClearMinusBtn.clicked.connect(
                lambda: operateOnCurrentStageCount(-1))
            courseClearMinusBtn.setObjectName("courseClearMinusBtn")

            btnEdit = PicButton(QPixmap('./imgs/editBtn.png'), self)
            btnEdit.resize(fontSize*2, fontSize*2)
            btnEdit.move(fontSize*18, 10)
            btnEdit.clicked.connect(lambda: toggleEditBtns(self))

            btnReset = PicButton(QPixmap('./imgs/reset.png'), self)
            btnReset.resize(fontSize*2, fontSize*2)
            btnReset.move(fontSize*20.5, 10)
            btnReset.clicked.connect(resetCurrentValues)
            btnReset.setObjectName("btnReset")

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


def toggleEditBtns(mainWindowObj):
    refreshAddBtn = mainWindowObj.findChild(
        PicButton, "refreshAddBtn")
    refreshMinusBtn = mainWindowObj.findChild(
        PicButton, "refreshMinusBtn")
    courseClearAddBtn = mainWindowObj.findChild(
        PicButton, "courseClearAddBtn")
    courseClearMinusBtn = mainWindowObj.findChild(
        PicButton, "courseClearMinusBtn")
    btnReset = mainWindowObj.findChild(
        PicButton, "btnReset")
    refreshAddBtn.show() if not refreshAddBtn.isVisible() else refreshAddBtn.hide()
    refreshMinusBtn.show() if not refreshMinusBtn.isVisible() else refreshMinusBtn.hide()
    courseClearAddBtn.show() if not courseClearAddBtn.isVisible() else courseClearAddBtn.hide()
    courseClearMinusBtn.show() if not courseClearMinusBtn.isVisible(
    ) else courseClearMinusBtn.hide()
    btnReset.show() if not btnReset.isVisible() else btnReset.hide()
