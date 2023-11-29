from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from videoReader import loggingStreaming
import sys
from PyQt5.QtGui import *
from logWriter import setupLogWriter
import configparser

config = configparser.ConfigParser()
config.read(r'config.ini', encoding="utf8")
targetStageCount = config.get('TestSettings', 'writeDownLogs') == "True"
if targetStageCount:
    setupLogWriter()
print("================")
print("Program start...")
app = QApplication(sys.argv)
app.setWindowIcon(QIcon(QPixmap('/imgs/icon550.ico')))
window = MainWindow()
loggingStreaming(window)
sys.exit("Program shut down noramlly.")
