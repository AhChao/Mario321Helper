# python builtin lib
import sys

# pip install lib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import configparser

# local py filefrom PyQt5.QtWidgets import *
from outlineLabel import OutlinedLabel
from picButton import PicButton
from videoReader import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        config.read(r'config.ini', encoding="utf8")
        gl.set_value("isDynamicDisplayMode", config.get(
            'DisplayConfig', 'isDynamicDisplayMode') == "True")

        # Init the window style
        self.setWindowFlag(Qt.FramelessWindowHint)
        if config.get('DisplayConfig', 'isBackgroundTransparent') == "True":
            self.setStyleSheet("background-color: rgba(255,255,255,0.5);")
            self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            self.setStyleSheet(
                r"background-image: url('./imgs/background_solid.png');")
        self.setWindowTitle("Mario321Helper")
        fontSize = int(config.get('DisplayConfig', 'fontSize'))

        # Init the label for displaying
        label = OutlinedLabel("0 / 15 刷  0 / 7 關", self)
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
            refreshAddBtn = CreatePicButton(
                imgPath="./imgs/addBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: operateOnCurrentRefreshCount(1),
                objName="refreshAddBtn"
            )

            refreshMinusBtn = CreatePicButton(
                imgPath="./imgs/subtractBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: operateOnCurrentRefreshCount(-1),
                objName="refreshMinusBtn"
            )
            courseClearAddBtn = CreatePicButton(
                imgPath="./imgs/addBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: operateOnCurrentStageCount(1),
                objName="courseClearAddBtn"
            )
            courseClearMinusBtn = CreatePicButton(
                imgPath="./imgs/subtractBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: operateOnCurrentStageCount(-1),
                objName="courseClearMinusBtn"
            )

            btnEdit = CreatePicButton(
                imgPath="./imgs/editBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: toggleEditBtns(self),
                objName="courseClearMinusBtn"
            )

            btnReset = CreatePicButton(
                imgPath="./imgs/reset.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: resetCurrentValues(),
                objName="btnReset"
            )

            btnExit = CreatePicButton(
                imgPath="./imgs/exitBtn.png",
                parentObj=self,
                btnSize=btnSize,
                clickevt=lambda: exitTheProgram(),
                objName="btnExit"
            )

            if gl.get_value("isDynamicDisplayMode"):
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
        if gl.get_value("isDynamicDisplayMode"):
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


def CreatePicButton(imgPath, parentObj, btnSize, clickevt, objName):
    btn = PicButton(QPixmap(imgPath), parentObj)
    btn.resize(btnSize, btnSize)
    btn.clicked.connect(clickevt)
    btn.setObjectName(objName)
    return btn
