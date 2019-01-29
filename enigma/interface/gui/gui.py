#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
from enigma.interface.gui.settings import *
from enigma.interface.gui.plugboard import *
import copy
import sys
from string import ascii_uppercase as alphabet
from re import sub


def letter_groups(text, group_size=5):
    output = ''
    i = 0
    for letter in text:
        if i == group_size:
            i = 0
            output += ' '
        output += letter
        i += 1
    return output


class Runtime:
    def __init__(self, api, cfg_load_plug):
        """
        Runtime object wrapping the root window
        :param api: {EnigmaAPI}
        :param cfg_load_plug: {callable} Returns loaded config
        """
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(
            QIcon(base_dir + 'enigma_200px.png')
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
            QIcon(base_dir + 'enigma_200px.png')
        )
        #self.setStyleSheet("QFrame{ border-radius: 5px}")
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
                                  self.o_textbox.sync_length,
                                  self._rotors.set_positions)

        # PLUGBOARD BUTTONS ====================================================

        plug_button = QPushButton('Plugboard')
        plug_button.setToolTip("Edit plugboard letter pairs")
        plug_button.clicked.connect(self.get_pairs)

        # PLUGS ================================================================

        self.cfg_load_plug = cfg_load_plug

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(lightboard)
        main_layout.addWidget(QLabel('INPUT', self))
        main_layout.addWidget(i_textbox)
        main_layout.addWidget(QLabel('OUTPUT', self))
        main_layout.addWidget(self.o_textbox)
        main_layout.addWidget(plug_button)

        self.show()
    
    def get_pairs(self):
        plugboard = Plugboard(self, self._api.plug_pairs)
        plugboard.exec()
        del plugboard

    def get_settings(self):
        pass


class Lightboard(QWidget):
    def __init__(self, master):
        super().__init__(master)

        # BASIC QT SETTINGS  ===================================================

        lb_layout = QVBoxLayout(self)
        lb_layout.setSpacing(10)
        frame = QFrame(self)

        # ATTRIBUTES ===========================================================

        self._lightbulbs = {}
        self._base_style = "QLabel{background-color: gray; color: %s;" \
                           "border: 1px solid black; border-radius: 10px;}"

        # CONSTRUCT LIGHTBOARD =================================================

        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)
            row_layout.setSpacing(10)

            for letter in row:
                ltr = alphabet[letter]
                label = QLabel(ltr, styleSheet=self._base_style % "black")

                self._lightbulbs[ltr] = label
                row_layout.addWidget(label)

            lb_layout.addWidget(row_frame)


    def power_off(self):
        for bulb in self._lightbulbs.values():
            bulb.setStyleSheet(self._base_style % "black")

    def light_up(self, letter):
        """
        Lights up letters on the lightboard, only powers off if letter not found
        :param letter: {char} Letter to light up
        """
        self.power_off()
        
        if letter in self._lightbulbs:
            self._lightbulbs[letter].setStyleSheet(self._base_style % "yellow")


class _RotorsHandler(QFrame):
    def __init__(self, master, position_plug, rotate_plug, enigma_api):
        """
        :param master: {Qt} Master qt object
        :param position_plug: {callable} Callable method for getting rotor positions
        :param rotate_plug: {callable} Temporary callable for getting rotor offset handlers
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._layout = QHBoxLayout(self)
        self._rotor_indicators = []

        for i in range(len(position_plug())):  # Rotor controls
            indicator = _RotorHandler(self, i, rotate_plug(i, 1, True), rotate_plug(i, -1, True), self.set_positions)
            self._layout.addWidget(indicator)
            self._rotor_indicators.append(indicator)
        
        # ATTRIBUTES ===========================================================

        self.enigma_api = enigma_api

        # SETTINGS ICON ========================================================

        button = QPushButton(QIcon(base_dir + 'settings.png'), '', self)
        button.setIconSize(QSize(50, 50))
        button.setToolTip("Edit Enigma rotor and reflector settings")
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button.clicked.connect(self.open_settings)

        # PLUGS ================================================================

        self.position_plug = position_plug
        self.set_positions()

        # SHOW WINDOW ==========================================================

        self._layout.addWidget(button)

    def open_settings(self):
        """
        Opens settings and reload afterwards
        """
        settings = Settings(self, self.enigma_api)
        settings.exec()  # Exec gives focus to top window, unlike .show
        self.set_positions()
        del settings

    def set_positions(self):
        """
        Refreshes position indicators to show new positions
        """
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
        self.set_positions = set_pos_plug

        # ROTATE FORWARD =======================================================

        position_plus = QPushButton('+', self)
        position_plus.clicked.connect(self.increment)
        position_plus.setToolTip("Rotates rotor forwards by one place")

        # POSITION INDICATOR ===================================================

        self._indicator = QLabel('A', self)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._indicator.setLineWidth(3)

        # ROTATE FORWARD =======================================================

        position_minus = QPushButton('-', self)
        position_minus.clicked.connect(self.decrement)
        position_minus.setToolTip("Rotates rotors backwards by one place")

        # SHOW WIDGETS =========================================================

        self._layout.addWidget(position_plus, alignment=Qt.AlignTop)
        self._layout.addWidget(self._indicator)
        self._layout.addWidget(position_minus, alignment=Qt.AlignBottom)

    def set(self, position):
        """
        Sets indicator position to specified text
        """
        self._indicator.setText(position)

    def increment(self):
        """
        Increments rotor position by one
        """
        self.plus_plug()
        self.set_positions()

    def decrement(self):
        """
        Decrements rotor position by one
        """
        self.minus_plug()
        self.set_positions()


class _InputTextBox(QTextEdit):
    def __init__(self, master, encrypt_plug, output_plug, sync_plug, refresh_plug):
        """
        Input textbox where text is entered, the last input letter is then encrypted and sent to
        the output widget
        :param master: {QWidget} Parent Qt object
        :param encrypt_plug: {callable} A callable that accepts one letter
                                        and returns one letter, should provide encryption
        :param output_plug: {callable} A callable that accepts one letter, should output it somewhere
        :param sync_plug: {callable} Sets output text widget to the desired length
        :param refresh_plug: {callable} A callable that should refresh a rotor positions
        """
        super().__init__(master)

        # QT WIDGET SETTINGS ===================================================

        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)

        # FONT =================================================================
        
        font = QFont("Monospace", 10)
        self.setFont(font)

        # PLUGS ================================================================

        self.encrypt_plug = encrypt_plug
        self.output_plug = output_plug
        self.sync_plug = sync_plug
        self.refresh_plug = refresh_plug

        # ATTRIBUTES ===========================================================

        self.last_len = 0

    def input_detected(self):
        """
        Responds to the text input event by encrypting the newly typed letter
        and sending it to the output text box.
        """
        text = self.toPlainText().upper()
        text = sub('[^A-Z]+', '', text)

        self.blockSignals(True)  # Blocks programatical edits to the widget
        self.setPlainText(letter_groups(text))
        self.moveCursor(QTextCursor.End)
        self.blockSignals(False)
        

        if len(text) > self.last_len:  # If text longer than before
            last_input = text[-1].upper()
            encrypted = self.encrypt_plug(last_input)

            self.output_plug(encrypted)
        else:
            self.sync_plug(len(text))

        self.last_len = len(text)

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
        self.setReadOnly(True)
        self.light_up_plug = light_up_plug

        # FONT =================================================================

        font = QFont("Monospace", 10)
        self.setFont(font)

    def sync_length(self, length):
        """
        Sets widget length to the desired length
        """
        self.light_up_plug('')
        text = letter_groups(self.toPlainText().replace(' ', '')[:length])
        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)

    def insert(self, letter):
        """
        Appends text into the textbox
        :param letter: {char} Letter to be appended
        """
        text = (self.toPlainText().replace(' ', '') + letter)
        self.setPlainText(letter_groups(text))
        self.moveCursor(QTextCursor.End)
        self.light_up_plug(letter)

