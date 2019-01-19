#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
import copy
import sys
from string import ascii_uppercase as alphabet


labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12', 'M-13',
          'N-14', 'O-15', 'P-16', 'Q-17', 'R-18', 'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26']

# For the GUI plug board
layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14], [0, 18, 3, 5, 6, 7, 9, 10], [15, 24, 23, 2, 21, 1, 13, 12, 11]]


class Runtime:
    """
    """
    def __init__(self, api, cfg_load_plug):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(QIcon('enigma/interface/assets/icons/enigma_200px.png'))
        self.root = Root(api, cfg_load_plug)
    
    def run(self):
        self.app.exec()


class Root(QWidget):
    """Root window for Enigma Qt GUI"""
    def __init__(self, enigma_api, cfg_load_plug):
        """
        Initializes Root QT window widgets
        """
        super().__init__()

        self.cfg_load_plug = cfg_load_plug
        main_layout = QVBoxLayout(self)
        self._api = enigma_api

        self.title = 'Enigma'
        self.setWindowTitle(self._api.model())
        self.setWindowIcon(QIcon('enigma/interface/assets/icons/enigma_200px.png'))
        #self.setStyleSheet("background-color: gray")  # TODO: Decide on stylesheet

        # Menu on top bar
        menu = QMenuBar(self)
        menu.addAction("Load", lambda: print(self.cfg_load_plug()))
        menu.addAction("Save", lambda: print("Save action"))
        menu.addAction("About", lambda: QDesktopServices.openUrl(QUrl("https://www.cryptomuseum.com/index.htm")))

        # ================
        # Rotors init
        self._rotors = _RotorsHandler(self, self._api.positions, self._api.rotate_rotor, enigma_api)

        # Lightboard frame
        lb_frame = QFrame(self)
        lb_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        lb_frame_layout = QGridLayout(lb_frame)
        lightboard = Lightboard(self)
        lb_frame_layout.addWidget(lightboard)

        # ===================================================================
        # INPUT OUTPUT FOR ENCRYPTION/DECRYPTION

        io_frame = QFrame(self)
        io_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        io_frame_layout = QGridLayout(io_frame)

        self.o_textbox = _OutputTextBox(self, lightboard.light_up, lightboard.power_off)
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
        plugboard = Plugboard(self)
        plug_button.clicked.connect(plugboard.show)
        main_layout.addWidget(plug_button)

        # ================
        # Rotors init
        main_layout.addWidget(plug_button)

        # ================

        self.setLayout(main_layout)
        QSound('enigma/interface/assets/sounds/click.wav').play()
        self.show()


class Lightboard(QWidget):
    def __init__(self, master):
        super().__init__(master)

        self.bulbs = {}
        lb_layout = QVBoxLayout(self)
        frame = QFrame(self)

        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)

            for letter in row:
                ltr = alphabet[letter]
                label = QLabel(alphabet[letter])
                label.setStyleSheet("QLabel{background-color: gray; border: 1px solid black; border-radius: 10px;}")
                self.bulbs[ltr] = label
                row_layout.addWidget(label)

            lb_layout.addWidget(row_frame)


    def light_up(self, letter):
        """
        Lights up letters on the lightboard
        """
        self.bulbs[letter].setStyleSheet("QLabel{color: yellow; background-color: gray; border: 1px solid black; border-radius: 10px;}")

    def power_off(self):
        """
        Disables the lit up letters
        """
        for bulb in self.bulbs.values():
            bulb.setStyleSheet("QLabel{background-color: gray; border: 1px solid black; border-radius: 10px;}")


class Plugboard(QDialog):
    def __init__(self, master):
        super().__init__(master)
        self.resize(200, 200)
        self.setWindowTitle("Settings")
        main_layout = QVBoxLayout(self)
        frame = QFrame(self)
        
        """
        self.plugs = {}
        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)

            for letter in row:
                label = QLabel(labels[letter])
                #label.setStyleSheet("QLabel{background-color: gray; border: 1px solid black; border-radius: 10px;}")
                self.plugs[letter] = label
                row_layout.addWidget(label)

            main_layout.addWidget(row_frame)
            """


class Settings(QDialog):
    def __init__(self, master, enigma_api):
        super().__init__(master)
        master_layout = QVBoxLayout(self)
        main_frame = QFrame(self)
        main_layout = QHBoxLayout(main_frame)
        self.setLayout(master_layout)

        img = QLabel("", self)
        img.setPixmap(QPixmap('enigma/interface/assets/icons/enigma1.jpg'))
        main_layout.addWidget(img)

        # Generate radios for components

        reflector_frame = QFrame(self)
        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        reflector_layout.addWidget(QLabel("REFLECTOR MODEL"), alignment=Qt.AlignTop)
        self.reflector_group = QButtonGroup()

        for i, model in enumerate(["UKW-B", "UKW-C"]):
            radio = QRadioButton(model, self)
            radio.setToolTip("Reflector is an Enigma component that \nreflects letters from the rotors back to the lightboard")
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        self.reflector_group.button(0).setChecked(True)
        main_layout.addWidget(reflector_frame)

        # Generate radio and ring settings
        self.radio_selectors = []
        self.ring_selectors = []
        for rotor in enigma_api.rotors():
            frame = QFrame(self)
            frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
            layout = QVBoxLayout(frame)
            
            button_group = QButtonGroup()
            layout.addWidget(QLabel("ROTOR MODEL"))
            for i, model in enumerate(["I", "II", "III", "IV", "V"]):
                radios = QRadioButton(model, self)
                button_group.addButton(radios)
                button_group.setId(radios, i)
                layout.addWidget(radios, alignment=Qt.AlignTop)
            button_group.button(0).setChecked(True)
            # Ringstellung combo box
            combobox = QComboBox(self)
            combobox.addItems(labels)

            layout.addWidget(QLabel("RING SETTING"))
            layout.addWidget(combobox, alignment=Qt.AlignBottom)
            self.ring_selectors.append(combobox)

            self.radio_selectors.append(button_group)
            main_layout.addWidget(frame)

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.collect)
        master_layout.addWidget(main_frame)
        master_layout.addWidget(apply_btn)
        master_layout.addWidget(QPushButton("Storno"))

        self.resize(200, 200)
        self.setWindowTitle("Settings")

    def collect(self):
        """
        Collects all data to be set
        """
        checked_ref = self.reflector_group.checkedButton() # REFLECTOR CHOICES
        if checked_ref is not None:
            print(checked_ref.text())
        else:
            print("Reflector not chosen")

        for group in self.radio_selectors:  # ROTOR CHOICES
            checked = group.checkedButton()
            if checked is not None:
                print(checked.text())
            else:
                print("Not checked!")

        for ring in self.ring_selectors:  # RING SETTING CHOICES
            print(ring.currentIndex())


class _RotorsHandler(QFrame):
    def __init__(self, master, position_plug, rotate_plug, enigma_api):
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

        settings = Settings(master, enigma_api)
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
        print("Incrementation of rotor nr. %d called!" % self._id)
        self.plus_plug()
        self.master.set_positions()

    def decrement(self):
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
    def __init__(self, master, light_up_plug, power_off_plug):
        super().__init__(master)
        self.setPlaceholderText("Encrypted message will appear here")
        self.light_up_plug = light_up_plug
        self.power_off_plug = power_off_plug

    def insert(self, letter):
        self.moveCursor(QTextCursor.End)
        self.power_off_plug()
        self.insertPlainText(letter)
        self.light_up_plug(letter)
