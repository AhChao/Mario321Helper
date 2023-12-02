from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from outlineLabel import OutlinedLabel
from picButton import PicButton
import configparser
from videoReader import *
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read(r'config.ini', encoding="utf8")
        isDynamicDisplayMode = config.get(
            'DisplayConfig', 'isDynamicDisplayMode') == "True"

        self.setWindowFlag(Qt.FramelessWindowHint)
        if config.get('DisplayConfig', 'isBackgroundTransparent') == "True":
            self.setStyleSheet("background-color: rgba(255,255,255,0.5);")
            self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            self.setStyleSheet(
                r"background-image: url('./imgs/background_solid.png');")
        self.setWindowTitle("Mario321Helper")
        label = OutlinedLabel("0 / 15 刷  0 / 7 關", self)

        fontSize = int(config.get('DisplayConfig', 'fontSize'))
        labelStyle = "font-family : Microsoft JhengHei;\
                    font-size: "+str(fontSize)+"pt;\
                    font-weight: bold;"
        label.setStyleSheet(labelStyle)
        label.adjustSize()
        self.label = label
        self.resize(450, 80)

        # init buttons
        if config.get('DisplayConfig', 'displayModifyButton') == "True":
            btnSize = 25
            btnBaseLine = fontSize + 45
            refreshAddBtn = PicButton(QPixmap('./imgs/addBtn.png'), self)
            refreshAddBtn.resize(btnSize, btnSize)
            refreshAddBtn.clicked.connect(
                lambda: operateOnCurrentRefreshCount(1))
            refreshAddBtn.setObjectName("refreshAddBtn")

            refreshMinusBtn = PicButton(
                QPixmap('./imgs/subtractBtn.png'), self)
            refreshMinusBtn.resize(btnSize, btnSize)
            refreshMinusBtn.clicked.connect(
                lambda: operateOnCurrentRefreshCount(-1))
            refreshMinusBtn.setObjectName("refreshMinusBtn")

            courseClearAddBtn = PicButton(QPixmap('./imgs/addBtn.png'), self)
            courseClearAddBtn.resize(btnSize, btnSize)
            courseClearAddBtn.clicked.connect(
                lambda: operateOnCurrentStageCount(1))
            courseClearAddBtn.setObjectName("courseClearAddBtn")

            courseClearMinusBtn = PicButton(
                QPixmap('./imgs/subtractBtn.png'), self)
            courseClearMinusBtn.resize(btnSize, btnSize)
            courseClearMinusBtn.clicked.connect(
                lambda: operateOnCurrentStageCount(-1))
            courseClearMinusBtn.setObjectName("courseClearMinusBtn")

            btnEdit = PicButton(QPixmap('./imgs/editBtn.png'), self)
            btnEdit.resize(btnSize, btnSize)
            btnEdit.clicked.connect(lambda: toggleEditBtns(self))

            btnReset = PicButton(QPixmap('./imgs/reset.png'), self)
            btnReset.resize(btnSize, btnSize)
            btnReset.clicked.connect(resetCurrentValues)
            btnReset.setObjectName("btnReset")

            btnExit = PicButton(QPixmap('./imgs/exitBtn.png'), self)
            btnExit.resize(btnSize, btnSize)
            btnExit.clicked.connect(exitTheProgram)
            btnExit.setObjectName("btnExit")

            if isDynamicDisplayMode:
                refreshAddBtn.move(fontSize*6, btnBaseLine)
                refreshMinusBtn.move(int(fontSize*7.5), btnBaseLine)
                courseClearAddBtn.move(fontSize*14, btnBaseLine)
                courseClearMinusBtn.move(int(fontSize*15.5), btnBaseLine)
                btnEdit.move(fontSize*18, 10)
                btnReset.move(int(fontSize*20.5), 10)
                btnExit.move(int(fontSize*23), 10)
            else:
                baseLine = 45
                functinoBtnBaseLine = 5
                refreshAddBtn.move(80, baseLine)
                refreshMinusBtn.move(119, baseLine)
                courseClearAddBtn.move(210, baseLine)
                courseClearMinusBtn.move(240, baseLine)
                btnReset.move(330, functinoBtnBaseLine)
                btnEdit.move(360, functinoBtnBaseLine)
                btnExit.move(390, functinoBtnBaseLine)

        self.show()

    def setTextToLabel(self, displayStr):
        self.label.setText(displayStr)
        config = configparser.ConfigParser()
        config.read(r'config.ini', encoding="utf8")
        if config.get('DisplayConfig', 'isDynamicDisplayMode') == "True":
            self.label.adjustSize()
        else:
            self.label.resize(350, 40)
        # self.adjustSize()

    def closeEvent(self, event):
        print("Main window is closed, shut down the whole program.")
        sys.exit("Program shut down noramlly.")


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
