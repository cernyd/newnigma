#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from enigma.interface.gui import *


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

        # ROTORS AND REFLECTOR SETTINGS ========================================
        
        self.generate_components(
            enigma_api.model_labels()['reflectors'],
            enigma_api.model_labels()['rotors']
        )

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

    def generate_components(self, reflectors, rotors):
        # REFLECTOR SETTINGS ===================================================
        
        reflector_frame = QFrame(self.settings_frame)
        reflector_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.addWidget(
            QLabel("REFLECTOR MODEL", reflector_frame), alignment=Qt.AlignTop
        )

        self.reflector_group = QButtonGroup(reflector_frame)
        for i, model in enumerate(reflectors):
            radio = QRadioButton(model, reflector_frame)
            radio.setToolTip("Reflector is an Enigma component that \nreflects "
                             "letters from the rotors back to the lightboard")
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        self.reflector_group.button(0).setChecked(True)

        self.settings_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

        self.radio_selectors = []
        self.ring_selectors = []

        for rotor in range(3):  # TODO: Generate correct rotor count
            rotor_frame = QFrame(self.settings_frame)
            rotor_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
            rotor_layout = QVBoxLayout(rotor_frame)
            rotor_frame.setLayout(rotor_layout)
            
            # ROTOR RADIOS =====================================================

            rotor_layout.addWidget(QLabel("ROTOR MODEL", rotor_frame))

            button_group = QButtonGroup(rotor_frame)
            for i, model in enumerate(rotors):
                radios = QRadioButton(model, rotor_frame)
                button_group.addButton(radios)
                button_group.setId(radios, i)
                rotor_layout.addWidget(radios, alignment=Qt.AlignTop)

            button_group.button(0).setChecked(True)
            
            # RINGSTELLUNG =====================================================

            combobox = QComboBox(rotor_frame)
            combobox.addItems(labels)

            hr = QFrame(rotor_frame)
            hr.setFrameShape(QFrame.HLine)
            hr.setFrameShadow(QFrame.Sunken)

            self.ring_selectors.append(combobox)
            self.radio_selectors.append(button_group)

            rotor_layout.addWidget(hr)
            rotor_layout.addWidget(QLabel("RING SETTING", rotor_frame))
            rotor_layout.addWidget(combobox, alignment=Qt.AlignBottom)

            self.settings_layout.addWidget(rotor_frame)

    def clear_components(self):
        while True:
            child = self.settings_layout.takeAt(0)
            if child:
                wgt = child.widget()
                wgt.deleteLater()
                del wgt
            else:
                break

        return
        del self.reflector_group
        self.reflector_group = None
        
        for rotor in self.radio_selectors:
            del rotor
        self.radio_selectors = None

        for ring in self.ring_selectors:
            del ring

        self.ring_selectors = None
    
    def regen_model(self, new_model):
        self.clear_components()

        self.generate_components(
            self.enigma_api.model_labels(new_model)['reflectors'],
            self.enigma_api.model_labels(new_model)['rotors']
        )

    def collect(self):
        """
        Collects all selected settings for rotors and other components,
        applies them to the enigma object
        """
        new_model = self.stacked_wikis.currently_selected
        new_reflector = self.reflector_group.checkedButton().text() # REFLECTOR CHOICES
        new_rotors = [group.checkedButton().text() for group in self.radio_selectors]
        ring_settings = [ring.currentIndex() for ring in self.ring_selectors]

        self.enigma_api.model(new_model)
        self.enigma_api.reflector(new_reflector)
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

        label = QLabel(model)
        label.setStyleSheet('font: 30px')

        self.title_layout.addWidget(label, alignment=Qt.AlignCenter)
        self.title_layout.addWidget(self.img)

        # MODEL WIKI ===========================================================

        self.wiki_text = QTextBrowser()
        self.wiki_text.setPlainText(self.description)  # setHtml sets html

        # BUTTONS ==============================================================

        self.select_button = QPushButton("Use this model")
        self.select_button.clicked.connect(lambda: select_plug(self.model))

        # SHOW WIDGETS =========================================================

        self.main_layout.addWidget(self.title_frame)
        self.main_layout.addWidget(self.wiki_text)
        self.main_layout.addWidget(self.select_button)
