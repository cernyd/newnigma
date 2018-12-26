#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from time import sleep


class Root(QWidget):
    def __init__(self):
        super().__init__()


        self.title = 'Enigma'
        self.setWindowTitle(self.title)
        

        # Menu
        menu = QMenuBar(self)
        menu.addMenu("Load")
        menu.addMenu("Save")

        # Layouts
        main_layout = QVBoxLayout(self)

        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(frame, alignment=Qt.AlignBottom)

        self.rotor_frame = QGridLayout(frame)

        # Rotors init
        self._rotor_indicators = []

        for i in range(3):
            indicator = QLabel('A', frame)
            indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            indicator.setLineWidth(3)
            self.rotor_frame.addWidget(indicator, 1, i, alignment=Qt.AlignTop)
            self.rotor_frame.addWidget(QPushButton('+', frame), 0, i, alignment=Qt.AlignTop)
            self.rotor_frame.addWidget(QPushButton('-', frame), 2, i, alignment=Qt.AlignTop)
            self._rotor_indicators.append(indicator)
        
        button = QPushButton('ROTORS', frame)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.rotor_frame.addWidget(button, 0, 3, 3, 1)

        self.setLayout(main_layout)

        self.show()



app = QApplication([])  # Qt runtime

root = Root()

app.exec_()
