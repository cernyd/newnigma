#!/usr/bin/env python3
"""Settings menu with tabs and associated objects, UKW_D menu."""
import logging

from PySide2.QtCore import Qt  # pylint: disable=no-name-in-module
from PySide2.QtGui import QPixmap  # pylint: disable=no-name-in-module
from PySide2.QtWidgets import \
    QComboBox  # pylint: disable=no-name-in-module; pylint: disable=no-name-in-module; pylint: disable=no-name-in-module; pylint: disable=no-name-in-module; pylint: disable=no-name-in-module
from PySide2.QtWidgets import (QButtonGroup, QDialog, QFrame, QHBoxLayout,
                               QLabel, QListWidget, QPushButton, QRadioButton,
                               QSizePolicy, QStackedWidget, QTabWidget,
                               QTextBrowser, QVBoxLayout, QWidget)

from enigma.interface.gui import LABELS, STYLESHEET, VIEW_DATA
from enigma.interface.gui.plugboard import Socket, _AbstractPlugboard

SELECTOR_LABELS = ("THIN", "SLOW", "MEDIUM", "FAST")
SELECTOR_TOOLTIPS = ("Does not rotate", None, None, "Rotates on every keypress")


class SettingsWindow(QDialog):
    """Settings menu with two tabs for settings models and components"""

    def __init__(self, master, enigma_api):
        """
        Submenu for setting Enigma model and component settings
        :param master: Qt parent object
        :param enigma_api: {EnigmaAPI}
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        main_layout = QVBoxLayout(self)
        self.__settings_frame = QFrame(self)
        self.__settings_layout = QHBoxLayout(self.__settings_frame)
        self.setWindowTitle("Settings")
        self.setLayout(main_layout)
        self.setFixedHeight(620)
        self.__reflector_group = []
        self.__rotor_frames = []

        # SAVE ATTRIBUTES ======================================================

        self.__enigma_api = enigma_api
        self.__rotor_selectors = []
        self.__ring_selectors = []
        self.__ukwd_window = UKWDSettingsWindow(self, enigma_api)

        # ROTORS AND REFLECTOR SETTINGS ========================================

        self.__ukwd_button = QPushButton("UKW-D pairs")
        self.__ukwd_button.clicked.connect(self.open_ukwd_window)

        # TAB WIDGET ===========================================================

        tab_widget = QTabWidget()

        self.__stacked_wikis = _ViewSwitcherWidget(self, self.regenerate_for_model)
        tab_widget.addTab(self.__stacked_wikis, "Enigma model")
        tab_widget.addTab(self.__settings_frame, "Component settings")

        # BUTTONS ==============================================================

        button_frame = QFrame(self)
        button_layout = QHBoxLayout(button_frame)
        button_layout.setAlignment(Qt.AlignRight)

        self.__apply_btn = QPushButton("Apply")
        self.__apply_btn.clicked.connect(self.collect)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.close)

        button_layout.addWidget(storno)
        button_layout.addWidget(self.__apply_btn)

        # SHOW WIDGETS =========================================================

        model_i = list(VIEW_DATA.keys()).index(self.__enigma_api.model())
        self.__stacked_wikis.select_model(model_i)
        self.__stacked_wikis.highlight(model_i)
        main_layout.addWidget(tab_widget)
        main_layout.addWidget(button_frame)

    def open_ukwd_window(self):
        """Opens UKWD wiring menu"""
        logging.info("Opened UKW-D wiring menu...")
        self.__ukwd_window.exec_()
        self.refresh_ukwd()

    def refresh_ukwd(self):
        """Refreshes Apply button according to criteria (UKW-D rotor must be
        selected to edit its settings)"""
        if self.__reflector_group.checkedButton().text() == "UKW-D":
            logging.info("UKW-D reflector selected, enabling UKW-D button...")

            if len(self.__ukwd_window.pairs()) != 12:
                self.__apply_btn.setDisabled(True)
                self.__apply_btn.setToolTip("Connect all 12 pairs in UKW-D wiring!")
            else:
                self.__apply_btn.setDisabled(False)
                self.__apply_btn.setToolTip(None)

            self.__ukwd_button.setDisabled(False)
            self.__ukwd_button.setToolTip("Select the UKW-D rotor to edit settings")
            if len(self.__rotor_frames) == 4:  # IF THIN ROTORS
                logging.info("Disabling thin rotor radiobuttons...")
                self.__rotor_frames[0].setDisabled(True)
        else:
            logging.info("UKW-D reflector deselected, disabling UKW-D button...")
            self.__apply_btn.setDisabled(False)
            self.__apply_btn.setToolTip(None)

            self.__ukwd_button.setDisabled(True)
            self.__ukwd_button.setToolTip(None)
            if len(self.__rotor_frames) == 4:  # IF THIN ROTORS
                logging.info("Enabling thin rotor radiobuttons...")
                self.__rotor_frames[0].setDisabled(False)

    def generate_components(self, reflectors, rotors, rotor_n):
        """Generates currently displayed components based on Enigma model
        :param reflectors: {str} Reflector labels
        :param rotors: {[str, str, str]} Rotor labels
        :param rotor_n: {int} Number of rotors the Enigma model has
        """
        # REFLECTOR SETTINGS ===================================================
        spacing = 15
        style = "font-size: 18px; text-align: center;"

        reflector_frame = QFrame(self.__settings_frame)
        reflector_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.setSpacing(spacing)
        reflector_layout.addWidget(
            QLabel("REFLECTOR", reflector_frame, styleSheet=style),
            alignment=Qt.AlignHCenter,
        )

        self.__reflector_group = QButtonGroup(reflector_frame)
        reflector_layout.setAlignment(Qt.AlignTop)

        for i, model in enumerate(reflectors):
            radio = QRadioButton(model, reflector_frame)
            radio.setToolTip(
                "Reflector is an Enigma component that \nreflects "
                "letters from the rotors back to the lightboard"
            )
            self.__reflector_group.addButton(radio)
            self.__reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        reflector_layout.addStretch()
        reflector_layout.addWidget(self.__ukwd_button)

        self.__reflector_group.button(0).setChecked(True)
        self.__reflector_group.buttonClicked.connect(self.refresh_ukwd)
        self.__settings_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

        self.__rotor_selectors = []
        self.__ring_selectors = []
        self.__rotor_frames = []

        for rotor in range(rotor_n):
            rotor_frame = QFrame(self.__settings_frame)
            rotor_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
            rotor_layout = QVBoxLayout(rotor_frame)
            rotor_layout.setAlignment(Qt.AlignTop)
            rotor_layout.setSpacing(spacing)
            rotor_frame.setLayout(rotor_layout)

            # ROTOR RADIOS =====================================================

            label = QLabel(
                SELECTOR_LABELS[-rotor_n:][rotor], rotor_frame, styleSheet=style
            )
            label.setToolTip(SELECTOR_TOOLTIPS[-rotor_n:][rotor])

            rotor_layout.addWidget(label, alignment=Qt.AlignHCenter)

            button_group = QButtonGroup(rotor_frame)

            final_rotors = rotors

            if "Beta" in rotors:
                logging.info("Enigma M4 rotors detected, adjusting radiobuttons...")
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
            for i, label in enumerate(LABELS):
                combobox.addItem(label, i)

            h_rule = QFrame(rotor_frame)
            h_rule.setFrameShape(QFrame.HLine)
            h_rule.setFrameShadow(QFrame.Sunken)

            self.__ring_selectors.append(combobox)
            self.__rotor_selectors.append(button_group)

            rotor_layout.addStretch()
            rotor_layout.addWidget(h_rule)
            rotor_layout.addWidget(
                QLabel("RING SETTING", rotor_frame, styleSheet=style),
                alignment=Qt.AlignHCenter,
            )
            rotor_layout.addWidget(combobox)

            self.__settings_layout.addWidget(rotor_frame)
            self.__rotor_frames.append(rotor_frame)

    def clear_components(self):
        """Deletes all components settings widgets"""
        while True:
            child = self.__settings_layout.takeAt(0)
            if not child:
                break
            wgt = child.widget()
            wgt.deleteLater()
            del wgt

    def regenerate_for_model(self, new_model):
        """Regenerates component settings
        :param new_model: {str} Enigma model
        """
        logging.info("Regenerating component settings...")
        self.clear_components()

        reflectors = self.__enigma_api.model_labels(new_model)["reflectors"]
        rotors = self.__enigma_api.model_labels(new_model)["rotors"]
        rotor_n = self.__enigma_api.rotor_n(new_model)

        self.generate_components(reflectors, rotors[::], rotor_n)

        defaults = self.__enigma_api.default_cfg(new_model, rotor_n)[1]
        for selected, i in zip(defaults, range(rotor_n)):
            self.__rotor_selectors[i].button(selected).setChecked(True)

        self.__ukwd_window.clear_pairs()
        self.__ukwd_window._old_pairs = {}
        if new_model == self.__enigma_api.model():
            self.load_from_api()
            self.__ukwd_window.refresh_pairs()
        self.refresh_ukwd()

    def load_from_api(self):
        """Loads displayed settings from shared EnigmaAPI instance"""
        logging.info("Loading component settings from EnigmaAPI...")

        model = self.__enigma_api.model()
        reflectors = self.__enigma_api.model_labels(model)["reflectors"]
        rotors = self.__enigma_api.model_labels(model)["rotors"]

        if "Beta" in rotors:
            rotors.remove("Beta")
            rotors.remove("Gamma")

        reflector_i = reflectors.index(self.__enigma_api.reflector())
        self.__reflector_group.button(reflector_i).setChecked(True)

        for i, rotor in enumerate(self.__enigma_api.rotors()):
            if (model == "Enigma M4" and self.__enigma_api.reflector() != "UKW-D" and i == 0):
                rotor_i = ["Beta", "Gamma"].index(rotor)
            else:
                rotor_i = rotors.index(rotor)

            self.__rotor_selectors[i].button(rotor_i).setChecked(True)

        for i, ring in enumerate(self.__enigma_api.ring_settings()):
            self.__ring_selectors[i].setCurrentIndex(ring - 1)

    def collect(self):
        """Collects all selected settings for rotors and other components,
        applies them to the EnigmaAPI as new settings"""
        logging.info("Collecting new settings...")

        new_model = self.__stacked_wikis.currently_selected
        new_reflector = self.__reflector_group.checkedButton().text()  # REFLECTOR CHOICES
        reflector_pairs = self.__ukwd_window.pairs()

        if new_reflector == "UKW-D" and new_model == "Enigma M4":
            new_rotors = [
                group.checkedButton().text() for group in self.__rotor_selectors[1:]
            ]
        else:
            new_rotors = [
                group.checkedButton().text() for group in self.__rotor_selectors
            ]

        ring_settings = [ring.currentIndex() + 1 for ring in self.__ring_selectors]

        logging.info(
            "EnigmaAPI state before applying settings:\n%s", str(self.__enigma_api)
        )

        if new_model != self.__enigma_api.model():
            self.__enigma_api.model(new_model)

        if new_reflector != self.__enigma_api.reflector():
            self.__enigma_api.reflector(new_reflector)

        if new_reflector == "UKW-D":
            self.__enigma_api.reflector_pairs(reflector_pairs)

        if new_rotors != self.__enigma_api.rotors():
            self.__enigma_api.rotors(new_rotors)

        if ring_settings != self.__enigma_api.ring_settings():
            self.__enigma_api.ring_settings(ring_settings)

        logging.info(
            "EnigmaAPI state when closing settings:\n%s", str(self.__enigma_api)
        )

        self.close()

    def pairs(self):
        """Returns current UKW-D pairs for collection"""
        return self._pairs


class _ViewSwitcherWidget(QWidget):
    """Object that handles displaying of Enigma model wikis and images"""

    def __init__(self, master, regen_plug):
        """
        :param master: Qt parent object
        :param regen_plug: {callable} Regenerates settings view to new contents
        """
        super().__init__(master)

        layout = QHBoxLayout()
        self.setLayout(layout)

        # LIST OF AVAILABLE MODELS =============================================

        self.model_list = QListWidget()
        self.model_list.setMaximumWidth(150)
        self.model_list.setMinimumWidth(150)
        self.model_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.model_list.currentRowChanged.connect(self.select_model)

        self.regen_plug = regen_plug

        # STACKED MODEL VIEWS ==================================================

        self.stacked_wikis = QStackedWidget()
        for i, model in enumerate(VIEW_DATA):
            self.model_list.insertItem(i, model)
            description = VIEW_DATA[model]["description"]
            self.stacked_wikis.addWidget(_EnigmaViewWidget(self, model, description))
        self.total_models = len(VIEW_DATA)

        layout.addWidget(self.model_list)
        layout.addWidget(self.stacked_wikis)

        # Sets initially viewed
        self.currently_selected = None

    def select_model(self, i):
        """Called when the "Use this model" button is pressed
        :param i: {str} Newly selected model index
        """
        logging.info('Changing settings view to model "%s"' % list(VIEW_DATA.keys())[i])
        model = list(VIEW_DATA.keys())[i]
        self.regen_plug(model)
        self.stacked_wikis.setCurrentIndex(i)

        self.model_list.blockSignals(True)
        self.model_list.setCurrentRow(i)
        self.model_list.blockSignals(False)

        self.currently_selected = model

    def highlight(self, i):
        """Highlights an option with Blue color, indicating that
        it is currently selected in EnigmaAPI
        :param i: {int} Index from list options
        """
        for index in range(self.total_models):
            item = self.model_list.item(index)
            item.setForeground(Qt.black)
            item.setToolTip(None)

        selected = self.model_list.item(i)
        selected.setBackground(Qt.gray)  # .setForeground(Qt.blue)
        selected.setToolTip("Currently used Enigma model")


class _EnigmaViewWidget(QWidget):
    """A single Enigma wiki view with text and image"""

    def __init__(self, master, model, description):
        """
        :param master: Qt parent object
        :param model: {str} Enigma model
        :param description: {str} Wiki text
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.setMargin(0)

        # MODEL IMAGE ==========================================================

        img = QLabel("")
        pixmap = QPixmap(VIEW_DATA[model]["img"]).scaled(400, 500)
        img.setPixmap(pixmap)
        img.setFrameStyle(QFrame.Panel | QFrame.Plain)
        img.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # MODEL WIKI ===========================================================

        wiki_text = QTextBrowser()
        wiki_text.setHtml(description)  # setHtml sets html
        wiki_text.setStyleSheet(STYLESHEET)
        wiki_text.setMinimumWidth(350)

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(img)
        main_layout.addWidget(wiki_text)


class UKWDSettingsWindow(_AbstractPlugboard):
    """UKW-D wiring settings derived from the abstract plugboard"""

    def __init__(self, master, enigma_api):
        """
        Settings menu for settings UKW-D wiring pairs
        :param master: Qt parent object
        :param enigma_api: {EnigmaAPI}
        """
        super().__init__(master, enigma_api, "UKW-D pairs")
        self._banned = ["J", "Y"]
        self._apply_plug = self.refresh_apply

        plug_frame = QFrame(self)
        plug_layout = QVBoxLayout(plug_frame)
        for group in "ABCDEF", "GHIKLM", "NOPQRS", "TUVWXZ":
            col_frame = QFrame(plug_frame)
            col_layout = QHBoxLayout(col_frame)
            col_layout.setMargin(0)

            for letter in group:
                socket = Socket(
                    self, letter, self.connect_sockets, self._enigma_api.charset()
                )
                col_layout.addWidget(socket)
                self._plugs[letter] = socket

            plug_layout.addWidget(col_frame)

        btn_frame = QFrame(self)
        btn_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setAlignment(Qt.AlignRight)

        self.__reset_all = QPushButton("Clear pairs")
        self.__reset_all.clicked.connect(self.clear_pairs)

        self.__apply_btn = QPushButton("Apply")
        self.__apply_btn.clicked.connect(self.apply)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.storno)

        btn_layout.addWidget(self.__reset_all)
        btn_layout.addWidget(storno)
        btn_layout.addWidget(self.__apply_btn)

        self._main_layout.addWidget(plug_frame)
        self._main_layout.addWidget(btn_frame)

        self.refresh_apply()

    def refresh_pairs(self):
        """Attempts to refresh visibly connected pairs from shared EnigmaAPI instance"""
        try:
            self.set_pairs(self._enigma_api.reflector_pairs())
        except ValueError:
            pass

    def refresh_apply(self):
        """Enables the "Apply" button only if all 12 pairs are connected"""
        if len(self.pairs()) != 12:
            self.__apply_btn.setDisabled(True)
            self.__apply_btn.setToolTip("All 12 pairs must be connected!")
            logging.info("Apply conditions met, Apply button enabled...")
        else:
            self.__apply_btn.setDisabled(False)
            self.__apply_btn.setToolTip(None)
            logging.info("Apply conditions met, Apply button enabled...")
