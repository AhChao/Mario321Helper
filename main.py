# python builtin lib
import sys

# pip install lib
import configparser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import *

# local py file
from mainWindow import MainWindow
from videoReader import initSettingValues, loggingStreaming
from logWriter import setupLogWriter
import globalVar as gl

config = configparser.ConfigParser()
config.read(r'config.ini', encoding="utf8")

# SetUp log writer for each print command
targetStageCount = config.get('TestSettings', 'writeDownLogs') == "True"
if targetStageCount:
    setupLogWriter()
gl._init()
print("================")
print("Program start...")
# Main window setup
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(QPixmap('/imgs/icon550.ico')))
window = MainWindow()
# Streaming logging
initSettingValues()
loggingStreaming(window)
# Normally wont reach, only prevent unhandeled exception thrown to here
sys.exit("Program shut down noramlly.")
