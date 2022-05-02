from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

MAX_BUTTON_WIDTH = 300


class LabeledInputGrid:
    widget = None
    grid_layout = None
    # layout.setColumnMinimumWidth(0, 100)
    input_count = 0

    def __init__(self, label_text, unit):
        self.label = QtWidgets.QLabel(label_text)
        self.label.setAlignment(Qt.AlignRight)
        self.unit = QtWidgets.QLabel(unit)
        self.input_txt = QtWidgets.QLineEdit("0")
        self.input_txt.setFixedWidth(100)
        self.input_txt.setAlignment(Qt.AlignRight)
        LabeledInputGrid.grid_layout.addWidget(self.label, LabeledInputGrid.input_count, 0)
        LabeledInputGrid.grid_layout.addWidget(self.input_txt, LabeledInputGrid.input_count, 1)
        LabeledInputGrid.grid_layout.addWidget(self.unit, LabeledInputGrid.input_count, 2)
        LabeledInputGrid.input_count += 1


def make_button(button_text):
    button = QtWidgets.QPushButton(button_text)
    button.setMaximumWidth(MAX_BUTTON_WIDTH)
    return button