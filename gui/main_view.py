import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import pyqtcss

from except_hook import ExceptHook
from comms.message_sender import MessageSender
from comms.messages import HummingBirdMessages

import logging
import threading

from gui_logging import GUILogger
from comms.tcp_handler import TCPHandler

class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_qt_connections()
        self.tcp_handler = TCPHandler()
        tcp_thread = threading.Thread(target=self.tcp_handler.tcp_listen)
        tcp_thread.daemon = True
        tcp_thread.start()
        self.sender = MessageSender(self.tcp_handler)

    def init_ui(self):
        self.setWindowTitle('Electronic Motion Library Test')

        # Message Sender for manual input
        self.send_input_txt = QtWidgets.QLineEdit()
        self.send_input_txt.setPlaceholderText("Enter message")

        # Configure send message button
        self.send_btn = QtWidgets.QPushButton("Send")

        # Layout send widgets
        send_widget = QtWidgets.QWidget()
        send_layout = QtWidgets.QHBoxLayout(send_widget)
        send_layout.addWidget(self.send_input_txt)
        send_layout.addWidget(self.send_btn)

        # Setup Program Control Buttons
        self.start_btn = QtWidgets.QPushButton("Start")
        self.pause_btn = QtWidgets.QPushButton("Pause")
        control_widget = QtWidgets.QWidget()
        control_layout = QtWidgets.QHBoxLayout(control_widget)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)

        # Setup console output
        self.gui_logger = GUILogger()
        self.console = self.gui_logger.text_edit
        logging.getLogger().addHandler(self.gui_logger)

        # Add everything to main layout
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.addWidget(send_widget)
        self.main_layout.addWidget(control_widget)
        self.main_layout.addWidget(self.console)

        self.setCentralWidget(self.main_widget)

    def setup_qt_connections(self):
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.pause_btn.clicked.connect(self.pause_btn_clicked)

    def send_btn_clicked(self):
        self.sender.send_message(self.send_input_txt.text())

    def start_btn_clicked(self):
        self.sender.send_message(HummingBirdMessages.START.value)

    def pause_btn_clicked(self):
        self.sender.send_message(HummingBirdMessages.PAUSE.value)

    def __del__(self):
        sys.stdout = sys.__stdout__


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.DEBUG)
    sys.excepthook = ExceptHook.excepthook
    app = QtWidgets.QApplication([])
    window = MainGUI()
    window.setStyleSheet(pyqtcss.get_style('dark_blue'))
    window.show()
    app.exit(app.exec_())