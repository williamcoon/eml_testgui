import logging
from PyQt5 import QtWidgets
from PyQt5 import QtGui

class GUILogger(logging.Handler):
    def __init__(self):
        super().__init__()
        self.text_edit = QtWidgets.QTextEdit()
        self.setFormatter(logging.Formatter(logging.basicConfig(
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)))

    def emit(self, record):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(f"{self.format(record)}\n")
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()