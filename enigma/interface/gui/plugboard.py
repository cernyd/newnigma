import PySide2 as qt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtMultimedia import *
from PySide2.QtGui import *
from enigma.interface.gui import *


class Plugboard(QDialog):
    def __init__(self, master, pairs_plug, enable_uhr_plug, disable_uhr_plug, uhr_position_plug):
        """
        Allows choosing and viewing current plugboard pairs
        :param master: Qt parent object
        :param pairs_plug: {callable} Provides access to setting and viewing plug
                                      pairs from api
        """
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

        # CONNECTS SOCKETS =====================================================
        
        self.pairs_plug = pairs_plug
        for pair in self.pairs_plug():
            self.connect_sockets(*pair)
        self.enable_uhr_plug = enable_uhr_plug
        self.disable_uhr_plug = disable_uhr_plug
        self.uhr_position_plug = uhr_position_plug

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
            pair_n = len(self._pairs())
            if pair_n != 10:
                self.apply_btn.setEnabled(False)
                self.apply_btn.setToolTip("When using the Uhr, exactly 10 plug pairs "
                                          "must be connected!\n%d pairs left to connect..." % (10 - pair_n))
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

    def _pairs(self):
        pairs = []
        for pair in self.pairs.items():
            if pair[::-1] not in pairs and all(pair):
                pairs.append(pair)
        return pairs

    def collect(self):
        """
        Collects all unique letter pairs
        """
        pairs = self._pairs()

        if self.enable_uhr.isChecked():
            self.enable_uhr_plug()
            self.uhr_position_plug(self.uhrmenu.position())

        self.pairs_plug(pairs)
        self.close()

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
        self.dial.setRange(0, 39)
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

    def position(self):
        return self.dial.value()

