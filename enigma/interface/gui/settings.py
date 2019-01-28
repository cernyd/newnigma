#!/usr/bin/env python3

import PyQt5 as qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import *
from enigma.interface.gui import *


class Settings(QDialog):
    def __init__(self, master, enigma_api):
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        master_layout = QVBoxLayout(self)
        main_frame = QFrame(self)
        main_layout = QHBoxLayout(main_frame)
        self.setWindowTitle("Settings")

        self.setLayout(master_layout)
        self.resize(200, 200)

        # SAVE ATTRIBUTES ======================================================

        self.enigma_api = enigma_api

        # REFLECTOR SETTINGS ===================================================

        reflector_frame = QFrame(self)
        reflector_frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        reflector_layout = QVBoxLayout(reflector_frame)
        reflector_layout.addWidget(
            QLabel("REFLECTOR MODEL"), alignment=Qt.AlignTop
        )
        reflector_labels = [ref['label'] for ref in enigma_api.model_data()['reflectors']]

        self.reflector_group = QButtonGroup()
        for i, model in enumerate(reflector_labels):
            radio = QRadioButton(model, self)
            radio.setToolTip("Reflector is an Enigma component that \nreflects "
                             "letters from the rotors back to the lightboard")
            self.reflector_group.addButton(radio)
            self.reflector_group.setId(radio, i)
            reflector_layout.addWidget(radio, alignment=Qt.AlignTop)

        self.reflector_group.button(0).setChecked(True)
        main_layout.addWidget(reflector_frame)

        # ROTOR SETTINGS =======================================================

        self.radio_selectors = []
        self.ring_selectors = []

        for rotor in enigma_api.rotors():
            frame = QFrame(self)
            frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
            layout = QVBoxLayout(frame)
            
            button_group = QButtonGroup()
            layout.addWidget(QLabel("ROTOR MODEL"))

            rotor_labels = [rotor['label'] for rotor in enigma_api.model_data()['rotors']]

            for i, model in enumerate(rotor_labels):
                radios = QRadioButton(model, self)
                button_group.addButton(radios)
                button_group.setId(radios, i)
                layout.addWidget(radios, alignment=Qt.AlignTop)

            button_group.button(0).setChecked(True)
            
            # Ringstellung combo box

            combobox = QComboBox(self)
            combobox.addItems(labels)
            hr = QFrame()
            hr.setFrameShape(QFrame.HLine)
            hr.setFrameShadow(QFrame.Sunken)
            layout.addWidget(hr)
            layout.addWidget(QLabel("RING SETTING"))
            layout.addWidget(combobox, alignment=Qt.AlignBottom)
            self.ring_selectors.append(combobox)

            self.radio_selectors.append(button_group)
            main_layout.addWidget(frame)

        # TAB WIDGET ===========================================================

        tab_widget = QTabWidget()
        self.models = ViewSwitcher(self, enigma_api.model)
        tab_widget.addTab(self.models, "Enigma Model")
        tab_widget.addTab(main_frame, "Component settings")

        # BUTTONS ==============================================================

        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.collect)

        storno = QPushButton("Storno")
        storno.clicked.connect(self.close)

        # SHOW WIDGETS =========================================================

        master_layout.addWidget(tab_widget)
        master_layout.addWidget(apply_btn)
        master_layout.addWidget(storno)

    def collect(self):
        """
        Collects all selected settings for rotors and other components,
        applies them to the enigma object
        """
        checked_ref = self.reflector_group.checkedButton() # REFLECTOR CHOICES

        new_model = self.models.currently_selected

        new_rotors = []
        for group in self.radio_selectors:  # ROTOR CHOICES
            checked = group.checkedButton()
            new_rotors.append(checked.text())

        ring_settings = []
        for ring in self.ring_selectors:  # RING SETTING CHOICES
            ring_settings.append(ring.currentIndex())

        print(new_model)
        self.enigma_api.model(new_model)
        self.enigma_api.reflector(checked_ref)
        self.enigma_api.rotors(new_rotors)
        self.enigma_api.ring_settings(ring_settings)

        self.close()


class ViewSwitcher(QWidget):
    def __init__(self, master, model_plug):
        super().__init__(master)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # =========================================

        self.model_list = QListWidget()
        self.model_list.currentRowChanged.connect(self.switch_view)

        # =========================================

        self.count = 0
        self.models = QStackedWidget()
        for model in view_data.keys():
            self.model_list.insertItem(self.count, model)
            self.models.addWidget(_EnigmaView(self, model, self.select_model))
            self.count += 1

        self.i = 0
        self.layout.addWidget(self.model_list)
        self.layout.addWidget(self.models)

        # Sets initially viewed
        selected = list(view_data.keys()).index(model_plug())

        self.models.setCurrentIndex(selected)
        self.model_list.item(selected).setSelected(True)

        self.currently_viewed = 0
        self.currently_selected = model_plug()

    def switch_view(self, i):
        self.models.setCurrentIndex(i)
        self.currently_viewed = i

    def select_model(self, model):
        self.currently_selected = model


class _EnigmaView(QWidget):
    def __init__(self, master, model, select_plug):
        super().__init__(master)

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

        # ======================================================================

        self.title_frame = QFrame(self)
        self.title_layout = QVBoxLayout(self.title_frame)
        label = QLabel(model)
        label.setStyleSheet('font: 30px')

        self.title_layout.addWidget(label, alignment=Qt.AlignCenter)
        self.title_layout.addWidget(self.img)

        # =========================================

        self.wiki_text = QTextBrowser()
        self.wiki_text.setPlainText(self.description)  # setHtml sets html

        # =========================================

        self.select_button = QPushButton("Use this model")
        self.select_button.clicked.connect(lambda: select_plug(self.model))

        # =========================================

        self.main_layout.addWidget(self.title_frame)
        self.main_layout.addWidget(self.wiki_text)
        self.main_layout.addWidget(self.select_button)
