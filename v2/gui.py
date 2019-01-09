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
    def __init__(self):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(QIcon('data/icons/enigma_200px.png'))
        self.root = Root()
    
    def run(self):
        self.app.exec()


class Root(QWidget):
    """

    """
    def __init__(self):
        """
        Initializes Root QT window widgets
        """
        super().__init__()


        self.title = 'Enigma'
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('data/icons/enigma_200px.png'))
        self.setStyleSheet("background-color: gray")
        

        # Menu on top bar
        menu = QMenuBar(self)
        menu.addMenu("Load")
        menu.addMenu("Save")
        menu.addMenu("About")

        # Frame for rotor control
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.rotor_frame = QHBoxLayout(frame)

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
        i_textbox = QTextEdit(self)
        i_textbox.setPlaceholderText("Type your message here")
        i_textbox.textChanged.connect(lambda: print("Input text changed!"))
        io_frame_layout.addWidget(i_textbox)

        io_frame_layout.addWidget(QLabel('OUTPUT', self))
        o_textbox = QTextEdit(self)
        o_textbox.setPlaceholderText("Encrypted message will appear here")
        o_textbox.setReadOnly(True)
        o_textbox.textChanged.connect(lambda: print("Output text changed!"))
        io_frame_layout.addWidget(o_textbox)


        # Main layout - whole window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(lb_frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(io_frame, alignment=Qt.AlignBottom)
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
        # Rotors init
        self._rotor_indicators = []

        for i in 1, 2, 3:  # Rotor controls
            indicator = RotorHandler(i, frame)
            self.rotor_frame.addWidget(indicator)
            self._rotor_indicators.append(indicator)
        
        button = QPushButton('ROTORS', frame)
        button.clicked.connect(lambda: print("ROTORS BUTTON CLICKED"))
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.rotor_frame.addWidget(button)

        # ================

        self.setLayout(main_layout)

        QSound('data/sounds/click.wav').play()

        self.show()


class RotorHandler(QFrame):
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

    def increment(self):
        self._indicator.setText('X')
        print("Incrementation of rotor nr. %d called!" % self._id)

    def decrement(self):
        self._indicator.setText('Y')
        print("Decrementation of rotor nr. %d called!" % self._id)
