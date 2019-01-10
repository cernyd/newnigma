#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
import copy
import sys


class Runtime:
    """
    """
    def __init__(self, api):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(QIcon('./assets/icons/enigma_200px.png'))
        self.root = Root(api)
    
    def run(self):
        self.app.exec()


class Root(QWidget):
    """Root window for Enigma Qt GUI"""
    def __init__(self, enigma_api):
        """
        Initializes Root QT window widgets
        """
        super().__init__()

        main_layout = QVBoxLayout(self)
        self._api = enigma_api

        self.title = 'Enigma'
        self.setWindowTitle(self._api.model())
        self.setWindowIcon(QIcon('./assets/icons/enigma_200px.png'))
        #self.setStyleSheet("background-color: gray")  # TODO: Decide on stylesheet

        # Menu on top bar
        menu = QMenuBar(self)
        menu.addMenu("Load")
        menu.addMenu("Save")
        menu.addMenu("About")

        # ================
        # Rotors init
        self._rotors = _RotorsHandler(self, self._api.rotors, self._api.positions)

        # Lightboard frame
        lb_frame = QFrame(self)
        lb_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        lb_frame_layout = QGridLayout(lb_frame)
        lb_frame_layout.addWidget(QLabel('LIGHTBOARD PLACEHOLDER', self))

        # IO frame
        io_frame = QFrame(self)
        io_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        io_frame_layout = QGridLayout(io_frame)

        io_frame_layout.addWidget(QLabel('INPUT', self))
        i_textbox = _InputTextBox(self)
        io_frame_layout.addWidget(i_textbox)

        io_frame_layout.addWidget(QLabel('OUTPUT', self))
        self.o_textbox = _OutputTextBox(self, i_textbox)
        io_frame_layout.addWidget(self.o_textbox)

        # Main layout - whole window
        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(lb_frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(io_frame, alignment=Qt.AlignBottom)


        # Plug and uhr buttons
        plug_button = QPushButton('Plugboard')
        plug_button.clicked.connect(lambda: print("PLUGBOARD BUTTON CLICKED"))
        uhr_button = QPushButton('Uhr')
        uhr_button.clicked.connect(lambda: print("UHR BUTTON CLICKED"))
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)

        # ================
        # Rotors init
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)

        # ================

        self.setLayout(main_layout)
        QSound('./assets/sounds/click.wav').play()
        self.show()


class Settings(QDialog):
    def __init__(self, master):
        super().__init__(master)
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.resize(200, 200)
        self.setWindowTitle("Settings")


class _RotorsHandler(QFrame):
    def __init__(self, master, rotors_plugin, position_plugin):
        super().__init__(master)

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._layout = QHBoxLayout(self)
        self._rotor_indicators = []

        for i in range(len(rotors_plugin())):  # Rotor controls
            indicator = _RotorHandler(i, self)
            self._layout.addWidget(indicator)
            self._rotor_indicators.append(indicator)
        
        rotor_icon = QIcon('./assets/icons/settings.png')
        button = QPushButton(rotor_icon, '', self)
        button.setIconSize(QSize(50, 50))

        settings = Settings(master)
        #button.clicked.connect(lambda: print("ROTORS BUTTON CLICKED"))
        button.clicked.connect(settings.show)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._layout.addWidget(button)
        self.position_plugin = position_plugin
        self.rotors_plugin = rotors_plugin
        self.set_positions()

    def set_positions(self):
        for rotor, position in zip(self._rotor_indicators, self.position_plugin()):
            rotor.set(position)


class _RotorHandler(QFrame):
    """Holds component references for particular rotor"""
    def __init__(self, i, master):
        super().__init__(master)
        self._id = i
        self._master = master
        self._layout = QVBoxLayout(self)

        position_plus = QPushButton('+', self)
        position_plus.clicked.connect(self.increment)
        self._layout.addWidget(position_plus, alignment=Qt.AlignTop)

        self._indicator = QLabel('A', self)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setLineWidth(3)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._layout.addWidget(self._indicator)

        position_minus = QPushButton('-', self)
        position_minus.clicked.connect(self.decrement)
        self._layout.addWidget(position_minus, alignment=Qt.AlignBottom)

    def set(self, position):
        self._indicator.setText(position)

    def increment(self):
        self._indicator.setText('X')
        print("Incrementation of rotor nr. %d called!" % self._id)

    def decrement(self):
        self._indicator.setText('Y')
        print("Decrementation of rotor nr. %d called!" % self._id)


class _InputTextBox(QTextEdit):
    def __init__(self, master):
        super().__init__(master)
        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)
        # TODO: Implement drag and drop maybe

    def input_detected(self):
        text = self.toPlainText()
        if len(text) == 0:
            print("Buffer empty!")
        else:
            print("You typed %s" % text[-1])


class _OutputTextBox(QTextEdit):
    def __init__(self, master, input_box):
        super().__init__(master)
        self.setPlaceholderText("Encrypted message will appear here")
        input_box.textChanged.connect(self.getter)
        self.setReadOnly(True)

    def getter(self):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText('X')
