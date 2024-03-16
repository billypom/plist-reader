import sys
import plistlib
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class PlistReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('plist-reader')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout.addWidget(self.textEdit)

        # Enable dropping onto the window
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for file_path in files:
            self.loadPlist(file_path)

    def loadPlist(self, file_path):
        try:
            with open(file_path, 'rb') as infile:
                plist = plistlib.load(infile)
                self.displayPlist(plist)
        except Exception as e:
            self.textEdit.append(f"Error: {e}")

    def displayPlist(self, plist):
        self.textEdit.clear()
        if isinstance(plist, dict):
            for item, value in plist.items():
                self.textEdit.append(f"[{item}]: {value}")
        else:
            self.textEdit.append("The file does not contain a valid plist dictionary.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlistReader()
    ex.show()
    sys.exit(app.exec_())
