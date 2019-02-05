#!/usr/bin/env python3

from time import sleep
from enigma.interface.gui import *
from enigma.interface.gui.settings import *
from enigma.interface.gui.plugboard import *
from string import ascii_uppercase as alphabet
from textwrap import wrap
from re import sub


class Runtime:
    def __init__(self, api, cfg_load_plug, cfg_save_plug):
        """
        Runtime object wrapping the root window
        :param api: {EnigmaAPI}
        :param cfg_load_plug: {callable} Returns loaded config
        :param cfg_save_plug: {callable} Allows to save data to config file
        """
        import sys
        self.app = QApplication(sys.argv)  # Needed for process name
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(
            QIcon(base_dir + 'enigma_200px.png')
        )
        self.root = Root(api, cfg_load_plug, cfg_save_plug)
    
    def run(self):
        self.app.exec_()


class Root(QWidget):
    """Root window for Enigma Qt GUI"""
    def __init__(self, enigma_api, cfg_load_plug, cfg_save_plug):
        """
        Initializes Root QT window widgets
        :param enigma_api: {EnigmaAPI} Initialized EnigmaAPI object
        :param cfg_load_plug: {callable} Returns loaded config
        :param cfg_save_plug: {callable} Allows to save data to config file
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

        self.enigma_api = enigma_api

        # MENU BAR =============================================================

        menu = QMenuBar(self)
        menu.addAction("Load Settings", self.load_config)
        menu.addAction("Save Settings", self.save_config)
        menu.addAction("Export message", self.export_message)
        url = QUrl("https://www.cryptomuseum.com/index.htm")
        menu.addAction("About", lambda: QDesktopServices.openUrl(url))

        # ROTORS INDICATOR =====================================================

        self._rotors = _RotorsHandler(self, self.enigma_api.positions, 
                                      self.enigma_api.generate_rotate_callback,
                                      self.enigma_api.rotate_reflector,
                                      enigma_api, self.refresh_gui,
                                      enigma_api.reflector_position)

        # LIGHTBOARD FRAME =====================================================

        lightboard = Lightboard(self)

        # INPUT OUTPUT FOR ENCRYPTION/DECRYPTION ===============================

        self.o_textbox = _OutputTextBox(self, lightboard.light_up, enigma_api.letter_group)
        self.i_textbox = _InputTextBox(self, enigma_api.encrypt, 
                                  self.o_textbox.insert,
                                  self.o_textbox.sync_length,
                                  self._rotors.set_positions,
                                  enigma_api.letter_group, enigma_api.revert_by)

        # PLUGBOARD BUTTONS ====================================================

        self.plug_button = QPushButton('Plugboard')
        self.plug_button.setToolTip("Edit plugboard letter pairs")
        self.plug_button.clicked.connect(self.get_pairs)

        # PLUGS ================================================================

        self.cfg_load_plug = cfg_load_plug
        self.cfg_save_plug = cfg_save_plug

        # SHOW WIDGETS =========================================================

        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(lightboard)
        main_layout.addWidget(QLabel('INPUT', self))
        main_layout.addWidget(self.i_textbox)
        main_layout.addWidget(QLabel('OUTPUT', self))
        main_layout.addWidget(self.o_textbox)
        main_layout.addWidget(self.plug_button)

        self.show()
    
    def get_pairs(self):
        plugboard = Plugboard(self, self.enigma_api)  # TODO: Refactor
        plugboard.exec()
        del plugboard
    
    def refresh_gui(self):
        self.setWindowTitle(self.enigma_api.model())
        self.i_textbox.clear()
        if self.enigma_api.data()['plugboard']:
            self.plug_button.show()
        else:
            self.plug_button.hide()

    def load_config(self):
        data = self.cfg_load_plug()
        self.enigma_api.load_from_config(data['saved'])
        self.i_textbox.blockSignals(True)
        self.refresh_gui()
        self.i_textbox.blockSignals(False)
        self._rotors.generate_rotors()
        self._rotors.set_positions()  # Refreshes positons... TODO: Maybe redundant?

    def save_config(self):
        data = self.enigma_api.get_config()
        old_data = self.cfg_load_plug()
        old_data['saved'] = data
        self.cfg_save_plug(old_data)

    def export_message(self):
        dialog = QFileDialog(self)
        filename = dialog.getSaveFileName(self, "Save enigma message")[0]

        if ".txt" not in filename and filename:  # TODO: Make less rudimentary
            QMessageBox.warning(self, "Overwrite warning", "Overwriting files that are not .txt textfiles is not permitted!")
        elif filename:
            with open(filename, 'w') as f:
                message = '\n'.join(wrap(self.o_textbox.text(), 29))
                f.write("%s\n%s\n" % (str(self.enigma_api), message))


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


class _RotorsHandler(QFrame):
    def __init__(self, master, position_plug, rotate_plug, rotate_ref_plug,
                 enigma_api, label_plug, reflector_pos_plug):
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
        self._reflector_indicator = None

        # ATTRIBUTES ===========================================================

        self.enigma_api = enigma_api
        self._rotate_plug = rotate_plug
        self._position_plug = position_plug
        self._label_plug = label_plug
        self._rotate_ref_plug = rotate_ref_plug
        self._reflector_pos_plug = reflector_pos_plug

        # SETTINGS ICON ========================================================

        self.settings_button = QPushButton(QIcon(base_dir + 'settings.png'), '', self)
        self.settings_button.setIconSize(QSize(50, 50))
        self.settings_button.setToolTip("Edit Enigma rotor and reflector settings")
        self.settings_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.settings_button.clicked.connect(self.open_settings)

        # GENERATE ROTORS AND REFLECTOR ========================================


        self.ukwd_indicator = QLabel("D")
        self.ukwd_indicator.setStyleSheet("color: red;")
        self.ukwd_indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.ukwd_indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.ukwd_indicator.setLineWidth(3)

        indicator = _RotorHandler(self, self._rotate_ref_plug(1, True),
                                  self._rotate_ref_plug(-1, True),
                                  self.set_positions)
        indicator.setStyleSheet("color: red;")

        self._layout.addWidget(indicator, alignment=Qt.AlignLeft)
        self._reflector_indicator = indicator
        self._layout.addWidget(self.settings_button)
        self._layout.addWidget(self.ukwd_indicator)

        self.generate_rotors()

        # PLUGS ================================================================

        self.set_positions()

    def generate_rotors(self):
        """
        Regenerates rotor views
        """
        # Delete

        self._layout.removeWidget(self.settings_button)

        for indicator in self._rotor_indicators:
            indicator.deleteLater()

        self._rotor_indicators = []

        if self.enigma_api.reflector_rotatable():
            self._reflector_indicator.show()
        else:
            self._reflector_indicator.hide()

        if self.enigma_api.reflector() == 'UKW-D':
            self.ukwd_indicator.show()
        else:
            self.ukwd_indicator.hide()

        # Create
        for i in range(len(self._position_plug())):  # Rotor controls
            indicator = _RotorHandler(self, self._rotate_plug(i, 1), self._rotate_plug(i, -1), self.set_positions)
            self._layout.addWidget(indicator, alignment=Qt.AlignLeft)
            self._rotor_indicators.append(indicator)

        self._layout.addWidget(self.settings_button)

    def open_settings(self):
        """
        Opens settings and reload afterwards
        """
        settings = Settings(self, self.enigma_api)
        settings.exec()  # Exec gives focus to top window, unlike .show
        self.set_positions()
        del settings
        self.generate_rotors()
        self._label_plug()

    def set_positions(self):
        """
        Refreshes position indicators to show new positions
        """
        if self.enigma_api.reflector_rotatable():
            self._reflector_indicator.set(self._reflector_pos_plug())

        for rotor, position in zip(self._rotor_indicators, self._position_plug()):
            rotor.set(position)


class _RotorHandler(QFrame):
    """Holds component references for particular rotor"""
    def __init__(self, master, plus_plug, minus_plug, set_pos_plug):
        """
        :param master: Qt parent object
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

        self.plus_plug = plus_plug
        self.minus_plug = minus_plug
        self.set_positions = set_pos_plug

        # ROTATE FORWARD =======================================================

        self.position_plus = QPushButton('+', self)
        self.position_plus.clicked.connect(self.increment)
        self.position_plus.setToolTip("Rotates rotor forwards by one place")

        # POSITION INDICATOR ===================================================

        self._indicator = QLabel('A', self)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._indicator.setLineWidth(3)

        # ROTATE FORWARD =======================================================

        self.position_minus = QPushButton('-', self)
        self.position_minus.clicked.connect(self.decrement)
        self.position_minus.setToolTip("Rotates rotors backwards by one place")

        # SHOW WIDGETS =========================================================

        self._layout.addWidget(self.position_plus, alignment=Qt.AlignTop)
        self._layout.addWidget(self._indicator)
        self._layout.addWidget(self.position_minus, alignment=Qt.AlignBottom)

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


def letter_groups(text, group_size=5):
    output = ''
    i = 0
    for letter in text:
        if i == group_size:
            i = 0
            output += ' '
        output += letter
        i += 1
    return output


class _InputTextBox(QPlainTextEdit):
    def __init__(self, master, encrypt_plug, output_plug, sync_plug, 
                 refresh_plug, letter_group_plug, revert_pos):
        """
        Handles user input and sends it to the output textbox
        :param master: {QWidget} Parent Qt object
        :param encrypt_plug: {callable} A callable that accepts one letter
                                        and returns one letter, should provide
                                        encryption
        :param output_plug: {callable} Accepts text that is to be displayed
        :param sync_plug: {callable} Synchronizes length of this
                                     widget with output widget
        :param refresh_plug: {callable} Refreshes displayed rotor positions
                                        a rotor positions
        :param letter_group_plug: {callable} Formats input text into blocks of
                                             n letters
        :param revert_pos: {callable} Reverts Enigma rotor position when the text
                                      gets shorter
        """
        super().__init__(master)

        # QT WIDGET SETTINGS ===================================================

        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)

        # FONT =================================================================
        
        font = QFont("Monospace", 10)
        self.setFont(font)

        # PLUGS ================================================================

        self.encrypt_plug = encrypt_plug
        self.output_plug = output_plug
        self.sync_plug = sync_plug
        self.refresh_plug = refresh_plug
        self.letter_group_plug = letter_group_plug
        self._revert_pos = revert_pos

        # ATTRIBUTES ===========================================================

        self.last_len = 0
        self._revert_pos = revert_pos
        
    def input_detected(self):
        """
        Encrypts newly typed/inserted text and outputs it to the output textbox
        """
        text = sub('[^A-Z]+', '', self.toPlainText().upper())
        
        new_len = len(text)
        diff = self.last_len - new_len
        self.last_len = new_len

        if diff < 0:  # If text longer than before
            self.output_plug(''.join(map(self.encrypt_plug, text[diff:])))
        else:
            self.sync_plug(new_len)
            self._revert_pos(diff)

        self.blockSignals(True)  # Blocks programatical edits to the widget
        self.setPlainText(letter_groups(text, self.letter_group_plug()))
        self.moveCursor(QTextCursor.End)
        self.blockSignals(False)

        self.refresh_plug()


class _OutputTextBox(QPlainTextEdit):
    def __init__(self, master, light_up_plug, letter_group_plug):
        """
        Shows text inserted trough the .insert() plug
        :param master: Qt parent object
        :param light_up_plug: {callable} Callable that accepts a single letter
                                         that should light up on the lightboard
        :param letter_group_plug: {callable} Formats input text into blocks of
                                             n letters
        """
        super().__init__(master)

        self.setPlaceholderText("Encrypted message will appear here")
        self.setReadOnly(True)
        self.light_up_plug = light_up_plug
        self.letter_group_plug = letter_group_plug

        # FONT =================================================================

        font = QFont("Monospace", 10)
        self.setFont(font)

    def sync_length(self, length):
        """
        Sets widget length to the desired length
        :param length: {int} new length of the displayed text
        """
        self.light_up_plug('')
        text = letter_groups(self.toPlainText().replace(' ', '')[:length], self.letter_group_plug())
        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)

    def insert(self, text):
        """
        Appends text into the textbox
        :param letter: {char} Letter to be appended
        """
        text = (self.toPlainText().replace(' ', '') + text)
        self.setPlainText(letter_groups(text, self.letter_group_plug()))
        self.moveCursor(QTextCursor.End)
        self.light_up_plug(text[-1])

    def text(self):
        """
        Returns currently displayed text
        """
        return self.toPlainText()

