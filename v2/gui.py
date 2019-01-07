#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
import sys


class Runtime:
    """
    """
    def __init__(self):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("TESt")
        self.app.setApplicationDisplayName("test")
        self.app.setOrganizationName("Test")
        self.app.setOrganizationDomain("Test")
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
        self.setWindowIcon(QIcon('data/icons/enigma.png'))
        

        # Menu on top bar
        menu = QMenuBar(self)
        menu.addMenu("Load")
        menu.addMenu("Save")
        menu.addMenu("About")

        # Frame for rotor control
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.rotor_frame = QGridLayout(frame)

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
        io_frame_layout.addWidget(QTextEdit(self))
        io_frame_layout.addWidget(QLabel('OUTPUT', self))
        io_frame_layout.addWidget(QTextEdit(self))

        # Main layout - whole window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(lb_frame, alignment=Qt.AlignBottom)
        main_layout.addWidget(io_frame, alignment=Qt.AlignBottom)
        plug_button = QPushButton('Plugboard')
        uhr_button = QPushButton('Uhr')
        uhr_button.setEnabled(False)
        plug_button.setEnabled(False)
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)


        # ================
        # Rotors init
        main_layout.addWidget(plug_button)
        main_layout.addWidget(uhr_button)


        # ================
        # Rotors init
        self._rotor_indicators = []

        for i in range(3):  # Rotor controls
            indicator = QLabel('A', frame)
            indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            indicator.setLineWidth(3)

            indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            
            self.rotor_frame.addWidget(indicator, 1, i, alignment=Qt.AlignTop)
            self.rotor_frame.addWidget(QPushButton('+', frame), 0, i, alignment=Qt.AlignTop)
            self.rotor_frame.addWidget(QPushButton('-', frame), 2, i, alignment=Qt.AlignTop)
            self._rotor_indicators.append(indicator)
        
        button = QPushButton('ROTORS', frame)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.rotor_frame.addWidget(button, 0, 3, 3, 1)

        # ================

        self.setLayout(main_layout)

        QSound('data/sounds/click.wav').play()

        self.show()
