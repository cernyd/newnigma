#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from time import sleep
from enigma.interface.gui.settings import *
import copy
import sys
from string import ascii_uppercase as alphabet
from re import sub


labels = [
    'A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09',
    'J-10', 'K-11', 'L-12', 'M-13', 'N-14', 'O-15', 'P-16', 'Q-17', 'R-18',
    'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26'
]

layout = [
    [16, 22, 4, 17, 19, 25, 20, 8, 14],
    [0, 18, 3, 5, 6, 7, 9, 10],
    [15, 24, 23, 2, 21, 1, 13, 12, 11]
]


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

        plugboard = Plugboard(self)
        plug_button = QPushButton('Plugboard')
        plug_button.setToolTip("Edit plugboard letter pairs")
        plug_button.clicked.connect(plugboard.exec)


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


class Plugboard(QDialog):
    def __init__(self, master):
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.resize(200, 200)
        self.setWindowTitle("Plugboard")
        main_layout = QVBoxLayout(self)
        frame = QFrame(self)
        self.setLayout(main_layout)

        # GENERATE PAIRS =======================================================
        
        self.pairs = {}
        self.plugs = {}
        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)

            for letter in row:
                letter = alphabet[letter]
                socket = Socket(row_frame, letter, self.connect_sockets, self.refresh_apply)
                self.plugs[letter] = socket
                self.pairs[letter] = None
                row_layout.addWidget(socket)

            main_layout.addWidget(row_frame)

        # BUTTONS ==============================================================

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.collect)
        storno = QPushButton("Storno")
        storno.clicked.connect(self.hide)

        self.uhr = QPushButton("Uhr")
        self.uhrmenu = Uhr(self)
        self.uhr.clicked.connect(self.uhrmenu.exec)

        self.enable_uhr = QCheckBox("Enable Uhr")  # In that case all plugs must be occupied! (and red/white)
        self.enable_uhr.stateChanged.connect(self.change_uhr_status)

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(storno)
        main_layout.addWidget(self.apply_btn)
        main_layout.addWidget(self.uhr)
        main_layout.addWidget(self.enable_uhr)

        self.change_uhr_status()

    def refresh_apply(self):
        """
        Refreshes the Apply button to see if conditions for it being enabled are
        met
        """
        if self.enable_uhr.isChecked():
            self.apply_btn.setEnabled(False)
            self.apply_btn.setToolTip("When using the Uhr, all plug pairs must be connected!")
        else:
            self.apply_btn.setEnabled(True)
            self.apply_btn.setToolTip(None)

    def change_uhr_status(self):
        """
        Enables "Uhr" button if the checkmark is enabled
        """
        self.refresh_apply()
        if self.enable_uhr.isChecked():
            self.uhr.setEnabled(True)
        else:
            self.uhr.setEnabled(False)
            self.uhr.setToolTip('Check "Enable Uhr" to enter Uhr settings')

    def collect(self):
        """
        Collects all unique letter pairs
        """
        pairs = []
        for pair in self.pairs.items():
            if pair[::-1] not in pairs and all(pair):
                pairs.append(pair)
        print(pairs)

    def connect_sockets(self, socket, other_socket):
        """
        Connects two cosckets without unnecessary interaction of two sockets
        to avoid recursive event calls)
        """
        if other_socket is None:
            other = self.pairs[socket]

            self.pairs[other] = None
            self.pairs[socket] = None
            self.plugs[socket].set_text('')
            self.plugs[other].set_text('')
        else:
            if self.pairs[other_socket] is not None:
                self.plugs[socket].set_text('')
            elif socket == other_socket:
                self.plugs[socket].set_text('')
            else:
                self.pairs[socket] = other_socket
                self.pairs[other_socket] = socket
                self.plugs[socket].set_text(other_socket)
                self.plugs[other_socket].set_text(socket)


class Socket(QFrame):
    def __init__(self, master, letter, connect_plug, apply_plug):
        """
        One sockets with label and text entry
        :param master: Qt parent object
        :param letter: Letter to serve as the label
        :param connect_plug: 
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        layout = QVBoxLayout(self)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        # ATTRIBUTES ===========================================================

        self.connect_plug = connect_plug
        self.letter = letter
        self.apply_plug = apply_plug
        self.connected_to = None

        # ENTRY ================================================================

        label = QLabel(letter)

        self.entry = QLineEdit()
        self.entry.setMaxLength(1)
        self.entry.textChanged.connect(self.entry_event)

        # SHOW WIDGETS

        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry)

    def entry_event(self):
        """
        Responds to a event when something changes in the plug entry
        """
        self.apply_plug()
        text = self.entry.text().upper()
        if self.entry.isModified():  # Prevents recursive event calls
            if text:
                 self.connect_plug(self.letter, text)
            else:
                 self.connect_plug(self.letter, None)

    def set_text(self, letter):
        """
        Sets text to the plug entrybox and sets white (vacant) or black
        (occupied) background color
        """
        if letter:
            self.entry.setStyleSheet("background-color: black; color: white")
        else:
            self.entry.setStyleSheet("background-color: white; color: black")
        self.entry.setText(letter)


class Uhr(QDialog):
    def __init__(self, master):
        """
        Uhr plugboard device
        :param master: Qt parent widget
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.setWindowTitle("Uhr")
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # UHR POSITION DIAL ====================================================

        self.indicator = QLabel("00")

        self.dial = QDial()
        self.dial.setWrapping(True)
        self.dial.setRange(1, 40)
        self.dial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dial.valueChanged.connect(self.refresh_indicator)

        # BUTTONS ==============================================================

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.close)

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(self.indicator, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.dial, alignment=Qt.AlignCenter)
        main_layout.addWidget(apply_btn)

    def refresh_indicator(self):
        """
        Sets displayed indicator value to current dial value
        """
        self.indicator.setText("%02d" % self.dial.value())

        
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
        

        # SETTINGS ICON ========================================================

        self.settings = Settings(master, enigma_api)

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
        self.settings.exec()  # Exec gives focus to top window, unlike .show
        self.set_positions()

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


class _InputTextBox(QPlainTextEdit):
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
        self.setPlainText(text)
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

    def sync_length(self, length):
        """
        Sets widget length to the desired length
        """
        self.light_up_plug('')
        self.setPlainText(self.toPlainText()[:length])

    def insert(self, letter):
        """
        Appends text into the textbox
        :param letter: {char} Letter to be appended
        """
        text = (self.toPlainText() + letter)

        self.moveCursor(QTextCursor.End)
        self.setPlainText(text)
        self.light_up_plug(letter)

