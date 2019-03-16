import logging

from PySide2.QtCore import Qt  # pylint: disable=no-name-in-module
from PySide2.QtWidgets import (QCheckBox, QDial, QDialog, QFrame, QHBoxLayout,  # pylint: disable=no-name-in-module
                               QLabel, QLineEdit, QPushButton, QSizePolicy,  # pylint: disable=no-name-in-module
                               QVBoxLayout)  # pylint: disable=no-name-in-module

from enigma.interface.gui import AbstractPlugboard, Socket


class PlugboardDialog(AbstractPlugboard):
    """Plugboard for setting Plugboard plug pairs in normal and Uhr mode"""

    def __init__(self, master, enigma_api):
        """
        Allows choosing and viewing current plugboard pairs
        :param master: Qt parent object
        :param enigma_api: {EnigmaAPI} Shared EnigmaAPI instance
        """
        super().__init__(master, enigma_api, "Plugboard")

        self.apply_plug = self.refresh_apply

        # GENERATE PAIRS =======================================================

        frame = QFrame(self)

        for row in enigma_api.data()["layout"]:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)
            row_layout.setMargin(0)

            for letter in row:
                letter = enigma_api.charset()[letter]
                socket = Socket(
                    row_frame, letter, self.connect_sockets, self.enigma_api.charset()
                )
                self.plugs[letter] = socket
                row_layout.addWidget(socket)

            self.main_layout.addWidget(row_frame)

        # BUTTONS ==============================================================

        self._button_frame = QFrame(self)
        self._button_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._button_layout = QHBoxLayout(self._button_frame)

        self.reset_all = QPushButton("Clear pairs")
        self.reset_all.clicked.connect(self.clear_pairs)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.collect)
        storno = QPushButton("Storno")
        storno.clicked.connect(self.hide)

        self.uhr = QPushButton("Uhr")
        self.uhrmenu = UhrDialog(self, enigma_api.uhr_position)
        self.uhr.clicked.connect(self.uhrmenu.exec)

        self.enable_uhr = QCheckBox(
            "Enable Uhr"
        )  # In that case all plugs must be occupied! (and red/white)
        self.enable_uhr.setChecked(enigma_api.uhr())
        self.enable_uhr.stateChanged.connect(self.change_uhr_status)

        # CONNECTS SOCKETS =====================================================

        self.enigma_api = enigma_api
        self.change_uhr_status(False)
        try:
            self.set_pairs(self.enigma_api.plug_pairs())
        except ValueError:
            pass

        # SHOW WIDGETS =========================================================

        self._button_layout.addWidget(self.enable_uhr)
        self._button_layout.addWidget(self.uhr)
        self._button_layout.addStretch()
        self._button_layout.addWidget(self.reset_all)
        self._button_layout.addWidget(storno)
        self._button_layout.addWidget(self.apply_btn)

        self.main_layout.addWidget(self._button_frame)

    def refresh_apply(self):
        """Enables "Apply" button either if Uhr is disabled or Uhr is enabled and
        10 pairs are set"""
        pair_n = len(self._pairs())
        if self.enable_uhr.isChecked() and pair_n != 10:
            logging.info("Uhr pre-requisites not met, keeping button disabled...")
            self.apply_btn.setDisabled(True)
            self.apply_btn.setToolTip(
                "When using the Uhr, exactly 10 plug pairs "
                "must be connected!\n%d pairs left to connect..." % (10 - pair_n)
            )
        else:
            logging.info("Apply conditions met, Apply button enabled...")
            self.apply_btn.setDisabled(False)
            self.apply_btn.setToolTip(None)

    def change_uhr_status(self, clear=True):
        """Enables "Uhr" button if the checkmark is enabled
        :param clear: {bool} Whether or not the connected pairs should be cleared
        """
        if clear:
            self.clear_pairs()
        self.refresh_apply()

        self.uhr_enabled = bool(self.enable_uhr.isChecked())
        self.uhr.setEnabled(self.uhr_enabled)
        if not self.uhr_enabled:
            self.uhr.setToolTip('Check "Enable Uhr" to enter Uhr settings')

    def collect(self):
        """Collects all unique letter pairs, enables and sets up Uhr if it's also checked"""
        pairs = self._pairs()

        if self.enable_uhr.isChecked():
            logging.info(
                "Connecting Uhr, setting position to %d", self.uhrmenu.position()
            )
            self.enigma_api.uhr("connect")
            self.enigma_api.uhr_position(self.uhrmenu.position())
        else:
            try:
                logging.info("Disconnecting Uhr...")
                self.enigma_api.uhr("disconnect")
            except ValueError:
                pass

        logging.info(
            'Setting plug pairs to "%s"', str(["".join(pair) for pair in pairs])
        )
        self.enigma_api.plug_pairs(pairs)
        self.close()


class UhrDialog(QDialog):
    """Uhr dialog menu with dial"""

    def __init__(self, master, uhr_position):
        """
        Uhr plugboard device
        :param master: Qt parent widget
        :param uhr_position: {callable} Sets the indicator to the current
                                        uhr position (if any)
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.setWindowTitle("Uhr")
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.setFixedSize(300, 400)

        # UHR POSITION DIAL ====================================================

        self.indicator = QLabel("00")
        self.indicator.setStyleSheet(
            "font-size: 20px; text-align: center; background-color: white"
        )
        self.indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.indicator.setFixedSize(40, 40)
        self.indicator.setLineWidth(2)

        self.dial = QDial()
        self.dial.setWrapping(True)
        self.dial.setRange(0, 39)
        self.dial.setFixedSize(280, 280)
        self.dial.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        position = 0
        try:
            position = uhr_position()
            logging.info("Successfully loaded Uhr position %d from plug...", position)
        except ValueError:
            logging.info("Failed loading Uhr position from plug, setting to 0...")

        self.dial.setValue(position)
        self._old_position = position
        self.indicator.setText("%02d" % position)
        self.dial.valueChanged.connect(self.refresh_indicator)

        # BUTTONS ==============================================================

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply)
        storno_btn = QPushButton("Storno")
        storno_btn.clicked.connect(self.storno)
        btn_frame = QFrame(self)
        btn_layout = QHBoxLayout(btn_frame)

        # SHOW WIDGETS =========================================================

        btn_layout.addWidget(storno_btn)
        btn_layout.addWidget(apply_btn)
        main_layout.addWidget(btn_frame)
        main_layout.addWidget(self.indicator, alignment=Qt.AlignHCenter)
        main_layout.addWidget(self.dial, alignment=Qt.AlignHCenter)
        main_layout.addWidget(btn_frame)

    def refresh_indicator(self):
        """Sets displayed indicator value to current dial value"""
        self.indicator.setText("%02d" % self.dial.value())

    def position(self):
        """Returns current Uhr dial setting"""
        return self.dial.value()

    def apply(self):
        """Sets currently selected position to be collected when applying settings"""
        self._old_position = self.dial.value()
        logging.info("New Uhr position %d applied, closing...", self._old_position)
        self.close()

    def storno(self):
        """Undoes current changes"""
        logging.info("Storno, reverting to old position %d...", self._old_position)
        self.dial.setValue(self._old_position)
        self.close()
