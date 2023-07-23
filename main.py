from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from videoReader import loggingStreaming
import sys
from PyQt5.QtGui import *


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(QPixmap('/imgs/icon550.png')))
window = MainWindow()
loggingStreaming(window)
# Start the event loop.
app.exec()
