import sys

from PyQt5.QtCore import Qt, QTimer
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
from gui.custom_gui import LabeledInputGrid, MAX_BUTTON_WIDTH, make_button

LENGTH_UNIT = "mm"
SPEED_UNIT = "mm/s"
ACCELERATION_UNIT = "mm/s^2"

CHECK_CONNECTION_INTERVAL = 1000 # ms


class MainGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.tcp_handler = TCPHandler()
        self.setup_qt_connections()
        tcp_thread = threading.Thread(target=self.tcp_handler.tcp_listen)
        tcp_thread.daemon = True
        tcp_thread.start()
        self.sender = MessageSender(self.tcp_handler)

        self.connected = False
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_tcp_connection)
        self.connection_timer.start(CHECK_CONNECTION_INTERVAL)

    def init_ui(self):
        self.setWindowTitle('Electronic Motion Library Test')

        # Message Sender for manual input
        self.send_input_txt = QtWidgets.QLineEdit()
        self.send_input_txt.setPlaceholderText("Enter message")

        # Configure send message button
        self.send_btn = make_button("Send")

        # Layout send widgets
        send_widget = QtWidgets.QWidget()
        send_layout = QtWidgets.QHBoxLayout(send_widget)
        send_layout.addWidget(self.send_input_txt)
        send_layout.addWidget(self.send_btn)

        # Setup Program Control Buttons
        self.start_btn = make_button("Start")
        self.pause_btn = make_button("Pause")

        control_widget = QtWidgets.QWidget()
        control_layout = QtWidgets.QHBoxLayout(control_widget)
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addStretch()

        # Setup console output
        self.gui_logger = GUILogger()
        self.console = self.gui_logger.text_edit
        logging.getLogger().addHandler(self.gui_logger)

        # Init recipe widget
        self.recipe_widget = self.get_recipe_widget()

        # Add everything to main layout
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.addWidget(send_widget)
        self.main_layout.addWidget(control_widget)
        self.main_layout.addWidget(self.recipe_widget)
        self.main_layout.addWidget(self.console)

        self.setCentralWidget(self.main_widget)

    def get_recipe_widget(self):
        LabeledInputGrid.widget = QtWidgets.QWidget()
        LabeledInputGrid.grid_layout = QtWidgets.QGridLayout(LabeledInputGrid.widget)
        recipe_widget = QtWidgets.QWidget()
        recipe_layout = QtWidgets.QVBoxLayout(recipe_widget)

        # Current Recipe Name
        self.recipe_name_txt = QtWidgets.QLineEdit()
        self.recipe_name_txt.setPlaceholderText("Recipe Name")
        self.recipe_name_txt.setMaximumWidth(MAX_BUTTON_WIDTH)

        # Recipe Parameters
        self.recipe_inputs = []
        self.x_origin_input = LabeledInputGrid("X Origin", LENGTH_UNIT)
        self.y_origin_input = LabeledInputGrid("Y Origin", LENGTH_UNIT)
        self.z_origin_input = LabeledInputGrid("Z Origin", LENGTH_UNIT)
        self.column_count = LabeledInputGrid("Number of Columns", "")
        self.row_count = LabeledInputGrid("Number of Rows", "")
        self.x_spacing_input = LabeledInputGrid("X Spacing", LENGTH_UNIT)
        self.y_spacing_input = LabeledInputGrid("Y Spacing", LENGTH_UNIT)
        self.z_plunge_depth = LabeledInputGrid("Z Plunge Depth", LENGTH_UNIT)
        self.dispense_time = LabeledInputGrid("Dispense Time", "s")
        self.max_speed = LabeledInputGrid("Maximum speed", SPEED_UNIT)
        self.max_accel = LabeledInputGrid("Maximum Acceleration", ACCELERATION_UNIT)

        self.recipe_inputs.append(self.x_origin_input)
        self.recipe_inputs.append(self.y_origin_input)
        self.recipe_inputs.append(self.z_origin_input)
        self.recipe_inputs.append(self.column_count)
        self.recipe_inputs.append(self.row_count)
        self.recipe_inputs.append(self.x_spacing_input)
        self.recipe_inputs.append(self.y_spacing_input)
        self.recipe_inputs.append(self.z_plunge_depth)
        self.recipe_inputs.append(self.dispense_time)
        self.recipe_inputs.append(self.max_speed)
        self.recipe_inputs.append(self.max_accel)

        recipe_inputs_widget = QtWidgets.QWidget()
        recipe_inputs_layout = QtWidgets.QHBoxLayout(recipe_inputs_widget)
        recipe_inputs_layout.addWidget(LabeledInputGrid.widget)
        recipe_inputs_layout.addStretch(1000)

        recipe_controls_widget = QtWidgets.QWidget()
        recipe_controls_layout = QtWidgets.QVBoxLayout(recipe_controls_widget)

        self.saved_recipes = QtWidgets.QComboBox()
        self.saved_recipes.setMaximumWidth(MAX_BUTTON_WIDTH)

        self.saved_recipes.addItem("Recipe 1")
        self.saved_recipes.addItem("Recipe 2")

        self.load_recipe_btn = make_button("Load Recipe")
        self.save_recipe_btn = make_button("Save Recipe")
        self.set_recipe_btn = make_button("Set Recipe")

        recipe_controls_layout.addWidget(self.saved_recipes)
        recipe_controls_layout.addWidget(self.load_recipe_btn)
        recipe_controls_layout.addWidget(self.set_recipe_btn)

        # Add widgets to recipe layout
        recipe_layout.setAlignment(Qt.AlignCenter)
        recipe_layout.addWidget(self.recipe_name_txt)
        recipe_layout.addWidget(self.save_recipe_btn)
        recipe_layout.addWidget(recipe_inputs_widget)
        recipe_layout.addWidget(recipe_controls_widget)
        recipe_layout.addStretch()

        return recipe_widget

    def setup_qt_connections(self):
        self.send_btn.clicked.connect(self.send_btn_clicked)
        self.start_btn.clicked.connect(self.start_btn_clicked)
        self.pause_btn.clicked.connect(self.pause_btn_clicked)
        self.save_recipe_btn.clicked.connect(self.save_recipe_btn_clicked)
        self.load_recipe_btn.clicked.connect(self.load_recipe_btn_clicked)
        self.set_recipe_btn.clicked.connect(self.set_recipe_btn_clicked)

    def check_tcp_connection(self):
        connected = self.tcp_handler.is_connected()
        if not connected:
            self.connected = False
        if connected and not self.connected:
            # New connection established, get recipes
            self.connected = True
            self.request_recipe_list()
        self.connection_timer.start(CHECK_CONNECTION_INTERVAL)

    def send_btn_clicked(self):
        self.sender.send_message(self.send_input_txt.text())

    def start_btn_clicked(self):
        self.sender.send_message(HummingBirdMessages.START.value)

    def pause_btn_clicked(self):
        self.sender.send_message(HummingBirdMessages.PAUSE.value)

    def save_recipe_btn_clicked(self):
        message = HummingBirdMessages.SAVE_RECIPE.value
        message += self.recipe_name_txt.text()
        for recipe_input in self.recipe_inputs:
            message += f",{recipe_input.input_txt.text()}"
        self.sender.send_message(message)

    def load_recipe_btn_clicked(self):
        message = HummingBirdMessages.LOAD_RECIPE.value
        message += self.saved_recipes.currentText()
        recipe = self.sender.send_message(message)
        if recipe is None:
            return

        self.recipe_name_txt.setText(self.saved_recipes.currentText())
        recipe_values = recipe.split(",")
        if len(recipe_values) != len(self.recipe_inputs):
            logging.error(f"Wrong number of recipe value returned: {len(recipe_values)} "
                          f"Expected: {len(self.recipe_inputs)}")
        index = 0
        for recipe_input in self.recipe_inputs:
            recipe_input.input_txt.setText(recipe_values[index])
            index += 1

    def set_recipe_btn_clicked(self):
        message = HummingBirdMessages.SET_CURRENT_RECIPE.value
        message += self.saved_recipes.currentText()
        self.sender.send_message(message)

    def request_recipe_list(self):
        message = HummingBirdMessages.LIST_RECIPES.value
        recipes = self.sender.send_message(message)
        recipe_list = recipes.split(",")
        self.set_recipe_list(recipe_list)

    def set_recipe_list(self, recipe_list):
        self.saved_recipes.clear()
        for recipe in recipe_list:
            self.saved_recipes.addItem(recipe)
        self.saved_recipes.setCurrentIndex(0)
        # Load the current recipe
        self.load_recipe_btn_clicked()

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