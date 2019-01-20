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
    def __init__(self, api, cfg_load_plug):
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(
            QIcon('enigma/interface/assets/icons/enigma_200px.png')
        )
        self.root = Root(api, cfg_load_plug)
    
    def run(self):
        self.app.exec()


class Root(QWidget):
    """Root window for Enigma Qt GUI"""
    def __init__(self, enigma_api, cfg_load_plug):
        """
        Initializes Root QT window widgets
        :param enigma_api: {EnigmaAPI} Initialized EnigmaAPI object
        :param cfg_load_plug: {callable} callable that returns loaded config
        """
        super().__init__()

        # QT WINDOW SETTINGS ===================================================

        self.title = 'Enigma'
        self.setWindowTitle(enigma_api.model())
        self.setWindowIcon(
            QIcon('enigma/interface/assets/icons/enigma_200px.png')
        )
        #self.setStyleSheet("background-color: gray")
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        
        # SAVE ATTRIBUTES ======================================================

        self._api = enigma_api

        # MENU BAR =============================================================

        menu = QMenuBar(self)
        menu.addAction("Load", lambda: print(self.cfg_load_plug()))
        menu.addAction("Save", lambda: print("Save action"))
        url = QUrl("https://www.cryptomuseum.com/index.htm")
        menu.addAction("About", lambda: QDesktopServices.openUrl(url))

        # ROTORS INDICATOR =====================================================

        self._rotors = _RotorsHandler(self, self._api.positions, 
                                      self._api.rotate_rotor, enigma_api)

        # LIGHTBOARD FRAME =====================================================

        lightboard = Lightboard(self)

        # INPUT OUTPUT FOR ENCRYPTION/DECRYPTION ===============================

        self.o_textbox = _OutputTextBox(self, lightboard.light_up)
        i_textbox = _InputTextBox(self, enigma_api.encrypt, 
                                  self.o_textbox.insert,
                                  self._rotors.set_positions)

        # PLUGBOARD BUTTONS ====================================================

        plugboard = Plugboard(self)
        plug_button = QPushButton('Plugboard')
        plug_button.setToolTip("Edit plugboard letter pairs")
        plug_button.clicked.connect(plugboard.show)

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(lightboard)
        main_layout.addWidget(QLabel('INPUT', self))
        main_layout.addWidget(i_textbox)
        main_layout.addWidget(QLabel('OUTPUT', self))
        main_layout.addWidget(self.o_textbox)
        main_layout.addWidget(plug_button)

        # PLUGS ================================================================

        self.cfg_load_plug = cfg_load_plug

        # SHOW WINDOW ==========================================================

        self.show()


class Lightboard(QWidget):
    def __init__(self, master):
        super().__init__(master)

        # BASIC QT SETTINGS  ===================================================

        lb_layout = QVBoxLayout(self)
        frame = QFrame(self)

        # ATTRIBUTES ===========================================================

        self._lightbulbs = {}
        self._base_style = "QLabel{background-color: gray; color: %s;" \
                           "border: 1px solid black; border-radius: 10px;}"

        # CONSTRUCT LIGHTBOARD =================================================

        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)

            for letter in row:
                ltr = alphabet[letter]
                label = QLabel(ltr, styleSheet=self._base_style % "black")

                self._lightbulbs[ltr] = label
                row_layout.addWidget(label)

            lb_layout.addWidget(row_frame)


    def light_up(self, letter):
        """
        Lights up letters on the lightboard
        :param letter: {char} Letter to light up
        """
        for bulb in self._lightbulbs.values():  # Power off all lightbulbs
            bulb.setStyleSheet(self._base_style % "black")

        self._lightbulbs[letter].setStyleSheet(self._base_style % "yellow")


class Plugboard(QDialog):
    def __init__(self, master):
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.resize(200, 200)
        self.setWindowTitle("Plugboard")
        main_layout = QVBoxLayout(self)
        frame = QFrame(self)
        self.setLayout = (main_layout)
        
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

        # QT WINDOW SETTINGS ===================================================

        master_layout = QVBoxLayout(self)
        main_frame = QFrame(self)
        main_layout = QHBoxLayout(main_frame)
        self.setWindowTitle("Settings")

        self.setLayout(master_layout)
        self.resize(200, 200)

        # SAMPLE IMAGE =========================================================

        #img = QLabel("", self)
        #img.setPixmap(QPixmap('enigma/interface/assets/icons/enigma1.jpg'))

        # REFLECTOR SETTINGS ===================================================

        reflector_frame = QFrame(self)
        reflector_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.addWidget(
            QLabel("REFLECTOR MODEL"), alignment=Qt.AlignTop
        )

        self.reflector_group = QButtonGroup()
        for i, model in enumerate(["UKW-B", "UKW-C"]):
            radio = QRadioButton(model, self)
            radio.setToolTip("Reflector is an Enigma component that \nreflects "
                             "letters from the rotors back to the lightboard")
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        self.reflector_group.button(0).setChecked(True)
        main_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

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

        # BUTTONS ==============================================================

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.collect)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.close)

        # SHOW WIDGETS =========================================================

        master_layout.addWidget(main_frame)
        master_layout.addWidget(apply_btn)
        master_layout.addWidget(storno)
        #main_layout.addWidget(img)

    def collect(self):
        """
        Collects all selected settings for rotors and other components,
        applies them to the enigma object
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

        self.close()


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
            indicator = _RotorHandler(self, i, rotate_plug(i, 1, True), rotate_plug(i, -1, True), self.set_positions)
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
    def __init__(self, master, i, plus_plug, minus_plug, set_pos_plug):
        """
        :param master: Qt parent object
        :param i: {int} Rotor index that determines fast/medium/slow rotor
        :param plus_plug: {callable} Callable that rotates the corresponding
                                     rotor one position forward
        :param minus_plug: {callable} Callable that rotates the corresponding
                                      rotor one position backward
        :param set_pos_plug: {callable} Callable that sets enigma object
                                        position to the current position
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self._layout = QVBoxLayout(self)
            
        # SAVE ATTRIBUTES ======================================================

        self._id = i
        self.plus_plug = plus_plug
        self.minus_plug = minus_plug
        self.master = master
        self.set_positions = set_pos_plug

        # ROTATE FORWARD =======================================================

        position_plus = QPushButton('+', self)
        position_plus.clicked.connect(self.increment)
        position_plus.setToolTip("Rotates rotor forwards by one place")

        # POSITION INDICATOR ===================================================

        self._indicator = QLabel('A', self)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._indicator.setLineWidth(8)

        # ROTATE FORWARD =======================================================

        position_minus = QPushButton('-', self)
        position_minus.clicked.connect(self.decrement)
        position_minus.setToolTip("Rotates rotors backwards by one place")

        # SHOW WIDGETS =========================================================

        self._layout.addWidget(position_plus, alignment=Qt.AlignTop)
        self._layout.addWidget(self._indicator)
        self._layout.addWidget(position_minus, alignment=Qt.AlignBottom)

    def set(self, position):
        self._indicator.setText(position)

    def increment(self):
        self.plus_plug()
        self.set_positions()

    def decrement(self):
        self.minus_plug()
        self.set_positions()


class _InputTextBox(QTextEdit):
    def __init__(self, master, encrypt_plug, output_plug, refresh_plug):
        """
        Input textbox where text is entered, the last input letter is then encrypted and sent to
        the output widget
        :param master: {QWidget} Parent Qt object
        :param encrypt_plug: {callable} A callable that accepts one letter
                                        and returns one letter, should provide encryption
        :param output_plug: {callable} A callable that accepts one letter, should output it somewhere
        :param refresh_plug: {callable} A callable that should refresh a rotor positions
        """
        super().__init__(master)

        # QT WIDGET SETTINGS ===================================================

        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)

        # PLUGS ================================================================

        self.encrypt_plug = encrypt_plug
        self.output_plug = output_plug
        self.refresh_plug = refresh_plug

    def input_detected(self):
        """
        Responds to the text input event by encrypting the newly typed letter
        and sending it to the output text box.
        """
        text = self.toPlainText()

        if len(text) > 0:
            last_input = text[-1].upper()
            encrypted = self.encrypt_plug(last_input)

            self.output_plug(encrypted)

        self.refresh_plug()


class _OutputTextBox(QTextEdit):
    def __init__(self, master, light_up_plug):
        """
        Shows text inserted trough the .insert() plug
        :param master: Qt parent object
        :param light_up_plug: {callable} Callable that accepts a single letter
                                         that should light up on the lightboard
        """
        super().__init__(master)

        self.setPlaceholderText("Encrypted message will appear here")
        self.light_up_plug = light_up_plug

    def insert(self, letter):
        """
        Appends text into the textbox
        :param letter: {char} Letter to be appended
        """
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(letter)
        self.light_up_plug(letter)
