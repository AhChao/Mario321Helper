from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
import sys

targetStageCount = 7
maxRefresh = 15

app = QApplication(sys.argv)
window = MainWindow()

# Start the event loop.
app.exec()
