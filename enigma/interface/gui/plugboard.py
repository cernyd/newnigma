from enigma.interface.gui import *


class Plugboard(AbstractPlugboard):
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

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.collect)
        storno = QPushButton("Storno")
        storno.clicked.connect(self.hide)

        self.uhr = QPushButton("Uhr")
        self.uhrmenu = Uhr(self, enigma_api._enigma.uhr_position)
        self.uhr.clicked.connect(self.uhrmenu.exec)

        self.enable_uhr = QCheckBox(
            "Enable Uhr"
        )  # In that case all plugs must be occupied! (and red/white)
        self.enable_uhr.setChecked(enigma_api.uhr())
        self.enable_uhr.stateChanged.connect(self.change_uhr_status)

        # CONNECTS SOCKETS =====================================================

        self.enigma_api = enigma_api

        for pair in self.enigma_api.plug_pairs():
            self.connect_sockets(*pair)

        # SHOW WIDGETS =========================================================

        self.main_layout.addWidget(storno)
        self.main_layout.addWidget(self.apply_btn)
        self.main_layout.addWidget(self.uhr)
        self.main_layout.addWidget(self.enable_uhr)

        self.change_uhr_status()

    def refresh_apply(self):
        """
        Enables "Apply" button either if Uhr is disabled or Uhr is enabled and
        10 pairs are set
        """
        if self.enable_uhr.isChecked():
            pair_n = len(self._pairs())
            if pair_n != 10:
                self.apply_btn.setEnabled(False)
                self.apply_btn.setToolTip(
                    "When using the Uhr, exactly 10 plug pairs "
                    "must be connected!\n%d pairs left to connect..." % (10 - pair_n)
                )
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
        Collects all unique letter pairs, enables and sets up Uhr if it's also
        checked
        """
        pairs = self._pairs()

        if self.enable_uhr.isChecked():
            self.enigma_api.uhr(True)
            self.enigma_api._enigma.uhr_position(self.uhrmenu.position())
        else:
            self.enigma_api.uhr(False)

        self.enigma_api.plug_pairs(pairs)
        self.close()


class Uhr(QDialog):
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

        # UHR POSITION DIAL ====================================================

        self._uhr_position = uhr_position

        try:
            self.indicator = QLabel(str(uhr_position()))
        except AssertionError:
            self.indicator = QLabel("00")

        self.dial = QDial()
        self.dial.setWrapping(True)
        self.dial.setRange(0, 39)

        try:
            self.dial.setValue(uhr_position())
        except AssertionError:
            pass

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
        """
        Returns current Uhr dial setting
        """
        return self.dial.value()
