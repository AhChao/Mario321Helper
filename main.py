from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
from videoReader import loggingStreaming
import sys


app = QApplication(sys.argv)
window = MainWindow()
loggingStreaming(window)
# Start the event loop.
app.exec()
