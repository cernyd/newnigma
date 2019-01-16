#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
import copy
import sys


labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12', 'M-13',
          'N-14', 'O-15', 'P-16', 'Q-17', 'R-18', 'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26']

# For the GUI plug board
layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14], [0, 18, 3, 5, 6, 7, 9, 10], [15, 24, 23, 2, 21, 1, 13, 12, 11]]


class Runtime:
    """
    """
    def __init__(self, api):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(QIcon('enigma/interface/assets/icons/enigma_200px.png'))
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
        self.setWindowIcon(QIcon('enigma/interface/assets/icons/enigma_200px.png'))
        #self.setStyleSheet("background-color: gray")  # TODO: Decide on stylesheet

        # Menu on top bar
        menu = QMenuBar(self)
        menu.addMenu("Load")
        menu.addMenu("Save")
        menu.addMenu("About")

        # ================
        # Rotors init
        self._rotors = _RotorsHandler(self, self._api.positions, self._api.rotate_rotor)

        # Lightboard frame
        lb_frame = QFrame(self)
        lb_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        lb_frame_layout = QGridLayout(lb_frame)
        lb_frame_layout.addWidget(QLabel('LIGHTBOARD PLACEHOLDER', self))

        # ===================================================================
        # INPUT OUTPUT FOR ENCRYPTION/DECRYPTION

        io_frame = QFrame(self)
        io_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        io_frame_layout = QGridLayout(io_frame)

        self.o_textbox = _OutputTextBox(self)
        #i_textbox = _InputTextBox(self, lambda l: 'Q', self.o_textbox)
        i_textbox = _InputTextBox(self, enigma_api.encrypt, self.o_textbox.insert)

        io_frame_layout.addWidget(QLabel('INPUT', self))
        io_frame_layout.addWidget(i_textbox)
        io_frame_layout.addWidget(QLabel('OUTPUT', self))
        io_frame_layout.addWidget(self.o_textbox)

        # ===================================================================

        # Main layout - whole window
        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(lb_frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(io_frame, alignment=Qt.AlignBottom)


        # Plug and uhr buttons
        plug_button = QPushButton('Plugboard')
        plug_button.setToolTip("Edit plugboard letter pairs")
        plug_button.clicked.connect(lambda: print("PLUGBOARD BUTTON CLICKED"))
        uhr_button = QPushButton('Uhr')
        uhr_button.setToolTip("Connect the Uhr extension and set pairs")
        uhr_button.clicked.connect(lambda: print("UHR BUTTON CLICKED"))
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)

        # ================
        # Rotors init
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)

        # ================

        self.setLayout(main_layout)
        QSound('enigma/interface/assets/sounds/click.wav').play()
        self.show()


class Settings(QDialog):
    def __init__(self, master):
        super().__init__(master)
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        img = QLabel("", self)
        pixmap = QPixmap('enigma/interface/assets/icons/enigma_200px.png')
        img.setPixmap(pixmap)

        main_layout.addWidget(img)
        main_layout.addWidget(QLabel("Created by David Cerny; 2018-2019", self))
        self.resize(200, 200)
        self.setWindowTitle("Settings")


class _RotorsHandler(QFrame):
    def __init__(self, master, position_plug, rotate_plug):
        """
        :param master: {Qt} Master qt object
        :param position_plug: {callable} Callable method for getting rotor positions
        :param rotate_plug: {callable} Temporary callable for getting rotor offset handlers
        """ # TODO: Change plus and minus plug to be more decoupled
        super().__init__(master)

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._layout = QHBoxLayout(self)
        self._rotor_indicators = []

        for i in range(len(position_plug())):  # Rotor controls
            indicator = _RotorHandler(i, self, rotate_plug(i, 1, True), rotate_plug(i, -1, True))
            self._layout.addWidget(indicator)
            self._rotor_indicators.append(indicator)
        
        rotor_icon = QIcon('enigma/interface/assets/icons/settings.png')
        button = QPushButton(rotor_icon, '', self)
        button.setIconSize(QSize(50, 50))
        button.setToolTip("Edit Enigma rotor and reflector settings")

        settings = Settings(master)
        #button.clicked.connect(lambda: print("ROTORS BUTTON CLICKED"))
        button.clicked.connect(settings.show)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._layout.addWidget(button)

        # PLUGS
        self.position_plug = position_plug

        self.set_positions()

    def set_positions(self):
        for rotor, position in zip(self._rotor_indicators, self.position_plug()):
            rotor.set(position)


class _RotorHandler(QFrame):
    """Holds component references for particular rotor"""
    def __init__(self, i, master, plus_plug, minus_plug):
        super().__init__(master)
        self._id = i
        self._master = master
        self._layout = QVBoxLayout(self)

        position_plus = QPushButton('+', self)
        position_plus.setToolTip("Rotates rotor forwards by one place")
        position_plus.clicked.connect(self.increment)
        self._layout.addWidget(position_plus, alignment=Qt.AlignTop)

        self._indicator = QLabel('A', self)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setLineWidth(3)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._layout.addWidget(self._indicator)

        self.plus_plug = plus_plug
        self.minus_plug = minus_plug
        position_minus = QPushButton('-', self)
        position_minus.setToolTip("Rotates rotors backwards by one place")
        position_minus.clicked.connect(self.decrement)

        self._layout.addWidget(position_minus, alignment=Qt.AlignBottom)
        self.master = master

    def set(self, position):
        self._indicator.setText(position)

    def increment(self):
        #self._indicator.setText('X')
        print("Incrementation of rotor nr. %d called!" % self._id)
        self.plus_plug()
        self.master.set_positions()

    def decrement(self):
        #self._indicator.setText('Y')
        print("Decrementation of rotor nr. %d called!" % self._id)
        self.minus_plug()
        self.master.set_positions()


class _InputTextBox(QTextEdit):
    def __init__(self, master, encrypt_plug, output_plug):
        super().__init__(master)
        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)
        self.encrypt_plug = encrypt_plug  # Decoupled plug for encryption
        self.output_plug = output_plug
        # TODO: Implement drag and drop maybe

    def input_detected(self):
        text = self.toPlainText()
        if len(text) > 0:
            last_input = text[-1].upper()
            encrypted = self.encrypt_plug(last_input)

            self.output_plug(encrypted)


class _OutputTextBox(QTextEdit):
    def __init__(self, master):
        super().__init__(master)
        self.setPlaceholderText("Encrypted message will appear here")
        #self.setReadOnly(True)

    def insert(self, letter):
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(letter)
