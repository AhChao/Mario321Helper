from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow
import sys

targetStageCount = 7
maxRefresh = 15
currentStageCount = 1
currentRefresh = 0

app = QApplication(sys.argv)
window = MainWindow()
displayStr = str(currentRefresh)+" / 15 刷  " + \
    str(currentStageCount) + " / 7 關"

window.setTextToLabel(displayStr)

# Start the event loop.
app.exec()
