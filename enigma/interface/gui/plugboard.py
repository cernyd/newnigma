from enigma.interface.gui import *
import logging


class PlugboardDialog(AbstractPlugboard):
    def __init__(self, master, enigma_api):
        """
        Allows choosing and viewing current plugboard pairs
        :param master: Qt parent object
        :param pairs_plug: {callable} Provides access to setting and viewing plug
                                      pairs from api
        """
        super().__init__(master, enigma_api, "Plugboard")

        # GENERATE PAIRS =======================================================
        frame = QFrame(self)

        for row in layout:
            row_frame = QFrame(frame)
            row_layout = QHBoxLayout(row_frame)

            for letter in row:
                letter = alphabet[letter]
                socket = Socket(
                    row_frame, letter, self.connect_sockets, self.refresh_apply
                )
                self.plugs[letter] = socket
                self.pairs[letter] = None
                row_layout.addWidget(socket)

            self.main_layout.addWidget(row_frame)

        # BUTTONS ==============================================================

        self._button_frame = QFrame(self)
        self._button_layout = QHBoxLayout(self._button_frame)

        self.reset_all = QPushButton("Clear pairs")
        self.reset_all.clicked.connect(self.set_pairs)

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
        self.set_pairs(self.enigma_api.plug_pairs())

        # SHOW WIDGETS =========================================================

        self._button_layout.addWidget(self.enable_uhr)
        self._button_layout.addWidget(self.uhr)
        self._button_layout.addStretch()
        self._button_layout.addWidget(self.reset_all)
        self._button_layout.addWidget(storno)
        self._button_layout.addWidget(self.apply_btn)

        self.main_layout.addWidget(self._button_frame)

        self.change_uhr_status()

    def refresh_pairs(self):
        try:
            self.set_pairs(self.enigma_api.plug_pairs())
        except ValueError:
            pass

    def refresh_apply(self):
        """
        Enables "Apply" button either if Uhr is disabled or Uhr is enabled and
        10 pairs are set
        """
        if self.enable_uhr.isChecked():
            pair_n = len(self._pairs())
            if pair_n != 10:
                self.apply_btn.setDisabled(True)
                self.apply_btn.setToolTip(
                    "When using the Uhr, exactly 10 plug pairs "
                    "must be connected!\n%d pairs left to connect..." % (10 - pair_n)
                )
            else:
                self.apply_btn.setDisabled(False)
                self.apply_btn.setToolTip(None)
        else:
            self.apply_btn.setDisabled(False)
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
        Collects all unique letter pairs, enables and sets up Uhr if it's also
        checked
        """
        pairs = self._pairs()

        if self.enable_uhr.isChecked():
            logging.info("Connecting Uhr, setting position to %d" % self.uhrmenu.position())
            self.enigma_api.uhr('connect')
            self.enigma_api.uhr_position(self.uhrmenu.position())
        else:
            try:
                logging.info("Disconnecting Uhr...")
                self.enigma_api.uhr('disconnect')
            except ValueError:
                pass

        logging.info('Setting plug pairs to "%s"' % str([''.join(pair) for pair in pairs]))
        self.enigma_api.plug_pairs(pairs)
        self.close()


class UhrDialog(QDialog):
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
        # self.setFixedSize(280, 400)

        # UHR POSITION DIAL ====================================================

        self._uhr_position = uhr_position

        try:
            self.indicator = QLabel(str(uhr_position()))
        except ValueError:
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
        self.dial.setFixedSize(300, 300)

        try:
            logging.info("Setting Uhr dial to position %d..." % uhr_position())
            self.dial.setValue(uhr_position())
        except ValueError:
            logging.info("No Uhr position, loading default...")

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
        """
        Returns current Uhr dial setting
        """
        return self.dial.value()
