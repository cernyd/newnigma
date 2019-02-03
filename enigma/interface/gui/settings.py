#!/usr/bin/env python3

import PySide2 as qt
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtMultimedia import *
from PySide2.QtGui import *
from enigma.interface.gui import *
from enigma.interface.gui.plugboard import Socket


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
        self.resize(200, 200)

        # SAVE ATTRIBUTES ======================================================

        self.enigma_api = enigma_api
        self.radio_selectors = []
        self.ring_selectors = []
        self.ukwd = UKWD_Settings(self)

        # ROTORS AND REFLECTOR SETTINGS ========================================
        
        self.ukwd_button = QPushButton("UKW-D Wiring")
        self.ukwd_button.clicked.connect(self.open_ukwd_wiring)
        self.regen_model(self.enigma_api.model(), True)

        # TAB WIDGET ===========================================================

        tab_widget = QTabWidget()

        self.stacked_wikis = ViewSwitcher(self, self.enigma_api.model, self.regen_model)
        tab_widget.addTab(self.stacked_wikis, "Enigma Model")
        tab_widget.addTab(self.settings_frame, "Component settings")

        # BUTTONS ==============================================================

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.collect)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.close)

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(tab_widget)
        main_layout.addWidget(apply_btn)
        main_layout.addWidget(storno)

        self.refresh_ukwd()

    def open_ukwd_wiring(self):
        self.ukwd.exec()

    def refresh_ukwd(self):
        if self.reflector_group.checkedButton().text() == 'UKW-D':
            self.ukwd_button.setDisabled(False)
            self.ukwd_button.setToolTip("Select the UKW-D rotor to edit settings")
            if len(self.rotor_frames) == 4:  # IF THIN ROTORS
                self.rotor_frames[0].setDisabled(True)
        else:
            self.ukwd_button.setDisabled(True)
            self.ukwd_button.setToolTip(None)
            if len(self.rotor_frames) == 4:  # IF THIN ROTORS
                self.rotor_frames[0].setDisabled(False)

    def generate_components(self, reflectors, rotors, rotor_n):
        # REFLECTOR SETTINGS ===================================================
        
        reflector_frame = QFrame(self.settings_frame)
        reflector_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.addWidget(
            QLabel("REFLECTOR", reflector_frame), alignment=Qt.AlignTop
        )

        reflectors.append("UKW-D")

        self.reflector_group = QButtonGroup(reflector_frame)
        for i, model in enumerate(reflectors):
            radio = QRadioButton(model, reflector_frame)
            radio.setToolTip("Reflector is an Enigma component that \nreflects "
                             "letters from the rotors back to the lightboard")
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        reflector_layout.addWidget(self.ukwd_button)

        self.reflector_group.button(0).setChecked(True)
        self.reflector_group.buttonClicked.connect(self.refresh_ukwd)
        self.settings_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

        self.radio_selectors = []
        self.ring_selectors = []
        self.rotor_frames = []

        for rotor in range(rotor_n):
            rotor_frame = QFrame(self.settings_frame)
            rotor_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
            rotor_layout = QVBoxLayout(rotor_frame)
            rotor_frame.setLayout(rotor_layout)
            
            # ROTOR RADIOS =====================================================

            label = QLabel(selector_labels[-rotor_n:][rotor], rotor_frame)
            label.setToolTip(selector_tooltips[-rotor_n:][rotor])

            rotor_layout.addWidget(label)

            button_group = QButtonGroup(rotor_frame)
            
            final_rotors = rotors

            if 'Beta' in rotors:
                if rotor == 0:
                    final_rotors = ['Beta', 'Gamma']
                else:
                    final_rotors.remove('Beta')
                    final_rotors.remove('Gamma')

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
            self.radio_selectors.append(button_group)

            rotor_layout.addWidget(hr)
            rotor_layout.addWidget(QLabel("RING SETTING", rotor_frame))
            rotor_layout.addWidget(combobox, alignment=Qt.AlignBottom)

            self.settings_layout.addWidget(rotor_frame)
            self.rotor_frames.append(rotor_frame)

    def clear_components(self):
        while True:
            child = self.settings_layout.takeAt(0)
            if child:
                wgt = child.widget()
                wgt.deleteLater()
                del wgt
            else:
                break
    
    def regen_model(self, new_model, from_api=False):
        """
        Regenerates component settings
        :param new_model: {str} Enigma model
        :param from_api: {boo} Sets settings to current api settings if True
        """
        self.clear_components()

        reflectors = self.enigma_api.model_labels(new_model)['reflectors']
        rotors = self.enigma_api.model_labels(new_model)['rotors']
        rotor_n = self.enigma_api.rotor_n(new_model)

        self.generate_components(
            reflectors,
            rotors[::],
            rotor_n
        )
        
        if from_api:
            reflector_i = reflectors.index(self.enigma_api.reflector())
            self.reflector_group.button(reflector_i).setChecked(True)
            
            for i, rotor in enumerate(self.enigma_api.rotors()):
                if 'Beta' in rotors:
                    if i == 0:
                        rotor_i = ['Beta', 'Gamma'].index(rotor)
                else:
                    rotor_i = rotors.index(rotor)

                self.radio_selectors[i].button(rotor_i).setChecked(True)
            
            for i, ring in enumerate(self.enigma_api.ring_settings()):
                self.ring_selectors[i].setCurrentIndex(ring-1)
        else:
            for i in range(rotor_n):
                self.radio_selectors[i].button(i).setChecked(True)

    def collect(self):
        """
        Collects all selected settings for rotors and other components,
        applies them to the enigma object
        """
        new_model = self.stacked_wikis.currently_selected
        new_reflector = self.reflector_group.checkedButton().text() # REFLECTOR CHOICES
        reflector_pairs = self.ukwd._pairs()
        new_rotors = [group.checkedButton().text() for group in self.radio_selectors]
        ring_settings = [ring.currentIndex()+1 for ring in self.ring_selectors]
        
        if new_model != self.enigma_api.model():
            self.enigma_api.model(new_model)

        self.enigma_api.reflector(new_reflector)
        if new_reflector == 'UKW-D':
            self.enigma_api._enigma.reflector_pairs(reflector_pairs)

        if new_rotors != self.enigma_api.rotors():
            self.enigma_api.rotors(new_rotors)

        self.enigma_api.ring_settings(ring_settings)

        self.close()


class ViewSwitcher(QWidget):
    def __init__(self, master, model_plug, regen_plug):
        """
        :param master: Qt parent object
        :param model_plug: {callable} Returns current enigma model
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
        for i, model in enumerate(view_data.keys()):
            self.model_list.insertItem(i, model)
            self.stacked_wikis.addWidget(_EnigmaView(self, model, self.select_model))

        self.layout.addWidget(self.model_list)
        self.layout.addWidget(self.stacked_wikis)

        # Sets initially viewed
        selected = list(view_data.keys()).index(model_plug())

        self.stacked_wikis.setCurrentIndex(selected)
        self.model_list.item(selected).setSelected(True)

        self.currently_selected = model_plug()

    def select_model(self, i):
        """
        Called when the "Use this model" button is pressed
        :param model: {str} Newly selected models
        """
        model = list(view_data.keys())[i]
        self.regen_plug(model)
        self.stacked_wikis.setCurrentIndex(i)
        self.currently_selected = model


class _EnigmaView(QWidget):
    def __init__(self, master, model, select_plug):
        """
        :param master: Qt parent object
        :param model: {str} Enigma model
        :param select_plug: {callable} Callback that accepts the newly selected 
                                       model
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        self.model = model
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # MODEL IMAGE ==========================================================

        self.description = view_data[model]['description']  # TODO: Decouple
        self.img = QLabel("")
        pixmap = QPixmap(view_data[model]['img']).scaled(300, 400)
        self.img.setPixmap(pixmap)
        self.img.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.img.setLineWidth(5)

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


class UKWD_Settings(QDialog):
    def __init__(self, master):
        super().__init__(master)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.resize(100, 150)
        self.setWindowTitle("UKW-D Wiring")

        self.pairs = {}  # TODO: Duplicate
        self.plugs = {}

        plug_frame = QFrame(self)
        plug_layout = QHBoxLayout(plug_frame)
        for group in 'ABCDEF', 'GHIKLM', 'NOPQRS', 'TUVWXZ':
            col_frame = QFrame(plug_frame)
            col_layout = QVBoxLayout(col_frame)

            for letter in group:
                socket = Socket(self, letter, self.connect_sockets, self.refresh_apply)
                col_layout.addWidget(socket)
                self.plugs[letter] = socket
                self.pairs[letter] = None
            
            plug_layout.addWidget(col_frame)

        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.close)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.storno)

        main_layout.addWidget(plug_frame)
        main_layout.addWidget(self.apply_btn)
        main_layout.addWidget(storno)

        self.refresh_apply()
    
    def storno(self):
        self.pairs = {}
        self.close()

    def refresh_apply(self):
        if len(self._pairs()) != 12:
            self.apply_btn.setDisabled(True)
            self.apply_btn.setToolTip("All 12 pairs must be connected!")
        else:
            self.apply_btn.setDisabled(False)
            self.apply_btn.setToolTip(None)
            

    def _pairs(self):  # TODO: Duplicate
        pairs = []
        for pair in self.pairs.items():
            if pair[::-1] not in pairs and all(pair):
                pairs.append(pair)
        return pairs

    def connect_sockets(self, socket, other_socket):  # TODO: Duplicate
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
            if other_socket in 'JY':
                self.plugs[socket].set_text('')
                return

            if self.pairs[other_socket] is not None:
                self.plugs[socket].set_text('')
            elif socket == other_socket:
                self.plugs[socket].set_text('')
            else:
                self.pairs[socket] = other_socket
                self.pairs[other_socket] = socket
                self.plugs[socket].set_text(other_socket)
                self.plugs[other_socket].set_text(socket)

