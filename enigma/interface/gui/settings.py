#!/usr/bin/env python3

from enigma.interface.gui import *
from enigma.interface.gui.plugboard import Socket
import logging

selector_labels = ("THIN", "SLOW", "MEDIUM", "FAST")
selector_tooltips = ("Does not rotate", None, None, "Rotates on every keypress")


class Settings(QDialog):
    def __init__(self, master, enigma_api):
        """
        Submenu for setting Enigma model and component settings
        :param master: Qt parent object
        :param enigma_api: {EnigmaAPI}
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        main_layout = QVBoxLayout(self)
        self.settings_frame = QFrame(self)
        self.settings_layout = QHBoxLayout(self.settings_frame)
        self.setWindowTitle("Settings")
        self.setLayout(main_layout)

        # SAVE ATTRIBUTES ======================================================

        self.enigma_api = enigma_api
        self.rotor_selectors = []
        self.ring_selectors = []
        self.ukwd = UKWD_Settings(self, enigma_api)

        # ROTORS AND REFLECTOR SETTINGS ========================================

        self.ukwd_button = QPushButton("UKW-D Wiring")
        self.ukwd_button.clicked.connect(self.open_ukwd_wiring)

        # TAB WIDGET ===========================================================

        tab_widget = QTabWidget()

        self.stacked_wikis = ViewSwitcher(self, self.regen_model)
        tab_widget.addTab(self.stacked_wikis, "Enigma Model")
        tab_widget.addTab(self.settings_frame, "Component settings")

        # BUTTONS ==============================================================

        self.button_frame = QFrame(self)
        self.button_layout = QHBoxLayout(self.button_frame)
        self.button_layout.setAlignment(Qt.AlignRight)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.collect)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.close)

        self.button_layout.addWidget(storno)
        self.button_layout.addWidget(self.apply_btn)

        # SHOW WIDGETS =========================================================

        self.stacked_wikis.select_model(list(view_data.keys()).index(self.enigma_api.model()))
        self.load_from_api()
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(self.button_frame)

        self.refresh_ukwd()

    def open_ukwd_wiring(self):
        """
        Opens UKWD wiring menu
        """
        logging.info("Opened UKW-D wiring menu...")
        self.ukwd.refresh_pairs()
        self.ukwd.exec_()
        self.refresh_ukwd()

    def refresh_ukwd(self):
        """
        Refreshes Apply button according to criteria (UKW-D rotor must be
        selected to edit its settings)
        """
        if self.reflector_group.checkedButton().text() == "UKW-D":
            logging.info("UKW-D reflector selected, enabling UKW-D button...")

            if len(self.ukwd._pairs()) != 12:
                self.apply_btn.setDisabled(True)
                self.apply_btn.setToolTip("Connect all 12 pairs in UKW-D wiring!")
            else:
                self.apply_btn.setDisabled(False)
                self.apply_btn.setToolTip(None)

            self.ukwd_button.setDisabled(False)
            self.ukwd_button.setToolTip("Select the UKW-D rotor to edit settings")
            if len(self.rotor_frames) == 4:  # IF THIN ROTORS
                logging.info("Disabling thin rotor radiobuttons...")
                self.rotor_frames[0].setDisabled(True)
        else:
            logging.info("UKW-D reflector deselected, disabling UKW-D button...")
            self.apply_btn.setDisabled(False)
            self.apply_btn.setToolTip(None)

            self.ukwd_button.setDisabled(True)
            self.ukwd_button.setToolTip(None)
            if len(self.rotor_frames) == 4:  # IF THIN ROTORS
                logging.info("Enabling thin rotor radiobuttons...")
                self.rotor_frames[0].setDisabled(False)

    def generate_components(self, reflectors, rotors, rotor_n):
        """
        Generates currently displayed components based on Enigma model
        :param reflectors: {str} Reflector labels
        :param rotors: {[str, str, str]} Rotor labels
        :param rotor_n: {int} Number of rotors the Enigma model has
        """
        # REFLECTOR SETTINGS ===================================================
        spacing = 15
        style = "font-size: 18px; text-align: center;"

        reflector_frame = QFrame(self.settings_frame)
        reflector_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.setSpacing(spacing)
        reflector_layout.addWidget(
            QLabel("REFLECTOR", reflector_frame, styleSheet=style),
            alignment=Qt.AlignHCenter
        )

        self.reflector_group = QButtonGroup(reflector_frame)
        reflector_layout.setAlignment(Qt.AlignTop)

        for i, model in enumerate(reflectors):
            radio = QRadioButton(model, reflector_frame)
            radio.setToolTip(
                "Reflector is an Enigma component that \nreflects "
                "letters from the rotors back to the lightboard"
            )
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        reflector_layout.addStretch()
        reflector_layout.addWidget(self.ukwd_button)

        self.reflector_group.button(0).setChecked(True)
        self.reflector_group.buttonClicked.connect(self.refresh_ukwd)
        self.settings_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

        self.rotor_selectors = []
        self.ring_selectors = []
        self.rotor_frames = []

        for rotor in range(rotor_n):
            rotor_frame = QFrame(self.settings_frame)
            rotor_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
            rotor_layout = QVBoxLayout(rotor_frame)
            rotor_layout.setAlignment(Qt.AlignTop)
            rotor_layout.setSpacing(spacing)
            rotor_frame.setLayout(rotor_layout)

            # ROTOR RADIOS =====================================================

            label = QLabel(
                selector_labels[-rotor_n:][rotor], rotor_frame,
                styleSheet=style
            )
            label.setToolTip(selector_tooltips[-rotor_n:][rotor])

            rotor_layout.addWidget(label, alignment=Qt.AlignHCenter)

            button_group = QButtonGroup(rotor_frame)

            final_rotors = rotors

            if "Beta" in rotors:
                logging.info("EnigmaM4 rotors detected, adjusting radiobuttons...")
                if rotor == 0:
                    final_rotors = ["Beta", "Gamma"]
                else:
                    final_rotors.remove("Beta")
                    final_rotors.remove("Gamma")

            for i, model in enumerate(final_rotors):
                radios = QRadioButton(model, rotor_frame)
                button_group.addButton(radios)
                button_group.setId(radios, i)
                rotor_layout.addWidget(radios, alignment=Qt.AlignTop)

            button_group.button(0).setChecked(True)

            # RINGSTELLUNG =====================================================

            combobox = QComboBox(rotor_frame)
            for i, label in enumerate(labels):
                combobox.addItem(label, i)

            hr = QFrame(rotor_frame)
            hr.setFrameShape(QFrame.HLine)
            hr.setFrameShadow(QFrame.Sunken)

            self.ring_selectors.append(combobox)
            self.rotor_selectors.append(button_group)

            rotor_layout.addStretch()
            rotor_layout.addWidget(hr)
            rotor_layout.addWidget(
                QLabel("RING SETTING", rotor_frame, styleSheet=style),
                alignment=Qt.AlignHCenter
            )
            rotor_layout.addWidget(combobox)

            self.settings_layout.addWidget(rotor_frame)
            self.rotor_frames.append(rotor_frame)

    def clear_components(self):
        """
        Deletes all components settings widgets
        """
        while True:
            child = self.settings_layout.takeAt(0)
            if not child:
                break
            wgt = child.widget()
            wgt.deleteLater()
            del wgt

    def regen_model(self, new_model):
        """
        Regenerates component settings
        :param new_model: {str} Enigma model
        :param from_api: {boo} Sets settings to current api settings if True
        """
        logging.info("Regenerating component settings...")
        self.clear_components()

        reflectors = self.enigma_api.model_labels(new_model)["reflectors"]
        rotors = self.enigma_api.model_labels(new_model)["rotors"]
        rotor_n = self.enigma_api.rotor_n(new_model)

        self.generate_components(reflectors, rotors[::], rotor_n)

        for selected, i in zip([0, 0, 1, 2][-rotor_n:], range(rotor_n)):
            self.rotor_selectors[i].button(selected).setChecked(True)

    def load_from_api(self):
        logging.info("Loading component settings from EnigmaAPI...")

        model = self.enigma_api.model()
        reflectors = self.enigma_api.model_labels()["reflectors"]
        rotors = self.enigma_api.model_labels()["rotors"]
        if "Beta" in rotors:
            rotors.remove("Beta")
            rotors.remove("Gamma")
        rotor_n = self.enigma_api.rotor_n()

        reflector_i = reflectors.index(self.enigma_api.reflector())
        self.reflector_group.button(reflector_i).setChecked(True)


        for i, rotor in enumerate(self.enigma_api.rotors()):
            if model == "EnigmaM4" and self.enigma_api.reflector() != "UKW-D" and i == 0:
                rotor_i = ["Beta", "Gamma"].index(rotor)
            else:
                rotor_i = rotors.index(rotor)

            self.rotor_selectors[i].button(rotor_i).setChecked(True)

        for i, ring in enumerate(self.enigma_api.ring_settings()):
            self.ring_selectors[i].setCurrentIndex(ring - 1)

    def collect(self):
        """
        Collects all selected settings for rotors and other components,
        applies them to the EnigmaAPI as new settings
        """
        logging.info("Collecting new settings...")

        new_model = self.stacked_wikis.currently_selected
        new_reflector = self.reflector_group.checkedButton().text()  # REFLECTOR CHOICES
        reflector_pairs = self.ukwd._pairs()

        if new_reflector == "UKW-D" and new_model == "EnigmaM4":
            new_rotors = [
                group.checkedButton().text() for group in self.rotor_selectors[1:]
            ]
        else:
            new_rotors = [
                group.checkedButton().text() for group in self.rotor_selectors
            ]

        ring_settings = [ring.currentIndex() + 1 for ring in self.ring_selectors]

        logging.info("EnigmaAPI state before applying settings:\n%s" % str(self.enigma_api))

        if new_model != self.enigma_api.model():
            self.enigma_api.model(new_model)

        if new_reflector != self.enigma_api.reflector():
            self.enigma_api.reflector(new_reflector)

        if new_reflector == "UKW-D":
            self.enigma_api._enigma.reflector_pairs(reflector_pairs)

        if new_rotors != self.enigma_api.rotors():
            self.enigma_api.rotors(new_rotors)

        if ring_settings != self.enigma_api.ring_settings():
            self.enigma_api.ring_settings(ring_settings)

        logging.info("EnigmaAPI state when closing settings:\n%s" % str(self.enigma_api))

        self.close()


class ViewSwitcher(QWidget):
    def __init__(self, master, regen_plug):
        """
        :param master: Qt parent object
        :param regen_plug: {callable} Regenerates settings view
        """
        super().__init__(master)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # LIST OF AVAILABLE MODELS =============================================

        self.model_list = QListWidget()
        self.model_list.currentRowChanged.connect(self.select_model)

        self.regen_plug = regen_plug

        # STACKED MODEL VIEWS ==================================================

        self.stacked_wikis = QStackedWidget()
        for i, model in enumerate(view_data):
            self.model_list.insertItem(i, model)
            description = view_data[model]["description"]
            self.stacked_wikis.addWidget(
                _EnigmaView(self, model, description)
            )

        self.layout.addWidget(self.model_list)
        self.layout.addWidget(self.stacked_wikis)

        # Sets initially viewed
        self.currently_selected = None

    def select_model(self, i):
        """
        Called when the "Use this model" button is pressed
        :param model: {str} Newly selected model
        """
        logging.info('Changing settings view to model "%s"' % list(view_data.keys())[i])
        model = list(view_data.keys())[i]
        self.regen_plug(model)
        self.stacked_wikis.setCurrentIndex(i)

        self.model_list.blockSignals(True)
        self.model_list.setCurrentRow(i)
        self.model_list.blockSignals(False)

        self.currently_selected = model


class _EnigmaView(QWidget):
    def __init__(self, master, model, description):
        """
        :param master: Qt parent object
        :param model: {str} Enigma model
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.model = model
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # MODEL IMAGE ==========================================================

        self.description = description
        self.img = QLabel("")
        pixmap = QPixmap(view_data[model]["img"]).scaled(300, 400)
        self.img.setPixmap(pixmap)
        self.img.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.img.setLineWidth(5)
        self.img.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # MODEL TITLE AND IMAGE ================================================

        self.title_frame = QFrame(self)
        self.title_layout = QVBoxLayout(self.title_frame)
        self.title_layout.addWidget(self.img)

        # MODEL WIKI ===========================================================

        self.wiki_text = QTextBrowser()
        self.wiki_text.setHtml(self.description)  # setHtml sets html
        self.wiki_text.setStyleSheet(stylesheet)

        # SHOW WIDGETS =========================================================

        self.main_layout.addWidget(self.title_frame)
        self.main_layout.addWidget(self.wiki_text)


class UKWD_Settings(AbstractPlugboard):
    def __init__(self, master, enigma_api):
        """
        Settings menu for settings UKW-D wiring pairs
        :param master: Qt parent object
        :param enigma_api: {EnigmaAPI}
        """
        super().__init__(master, enigma_api, "UKW-D Wiring")
        self.banned = ["J", "Y"]

        plug_frame = QFrame(self)
        plug_layout = QVBoxLayout(plug_frame)
        for group in "ABCDEF", "GHIKLM", "NOPQRS", "TUVWXZ":
            col_frame = QFrame(plug_frame)
            col_layout = QHBoxLayout(col_frame)

            for letter in group:
                socket = Socket(self, letter, self.connect_sockets, self.refresh_apply)
                col_layout.addWidget(socket)
                self.plugs[letter] = socket
                self.pairs[letter] = None

            plug_layout.addWidget(col_frame)

        btn_frame = QFrame(self)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setAlignment(Qt.AlignRight)

        self.reset_all = QPushButton("Clear pairs")
        self.reset_all.clicked.connect(self.set_pairs)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.close)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.storno)

        btn_layout.addWidget(self.reset_all)
        btn_layout.addWidget(storno)
        btn_layout.addWidget(self.apply_btn)

        self.main_layout.addWidget(plug_frame)
        self.main_layout.addWidget(btn_frame)

        self.refresh_apply()

    def refresh_pairs(self):
        try:
            self.set_pairs(self.enigma_api.reflector_pairs())
        except ValueError:
            pass

    def refresh_apply(self):
        """
        Enables the "Apply" button only if all 12 pairs are connected
        """
        if len(self._pairs()) != 12:
            self.apply_btn.setDisabled(True)
            self.apply_btn.setToolTip("All 12 pairs must be connected!")
        else:
            self.apply_btn.setDisabled(False)
            self.apply_btn.setToolTip(None)
