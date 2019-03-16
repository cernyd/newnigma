import logging
from copy import copy
from re import findall, sub
from textwrap import wrap

from enigma.interface.gui import *
from enigma.interface.gui.plugboard import *
from enigma.interface.gui.settings import *


class Runtime:
    def __init__(self, api):
        """Runtime object wrapping the root window
        :param api: {EnigmaAPI}
        """
        from sys import argv

        logging.info("Setting application icon and title...")

        self.app = QApplication(argv)
        self.app.setApplicationName("Enigma")
        self.app.setApplicationDisplayName("Enigma")
        self.app.setWindowIcon(QIcon(base_dir + "enigma_200px.png"))

        Root(api)
        logging.info("Starting Qt runtime...")
        self.app.exec_()


class Root(QWidget):
    """Root window for Enigma Qt GUI"""

    def __init__(self, enigma_api):
        """Initializes Root QT window widgets
        :param enigma_api: {EnigmaAPI} Initialized EnigmaAPI object
        """
        super().__init__()

        # QT WINDOW SETTINGS ==================================================

        self.setWindowIcon(QIcon(base_dir + "enigma_200px.png"))
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        # SAVE ATTRIBUTES =====================================================

        self.enigma_api = enigma_api
        logging.info("Qt GUI initialized with EnigmaAPI settings:\n%s" % str(enigma_api))

        # MENU BAR ============================================================

        menu = QMenuBar(self)
        save_load_menu = menu.addMenu("Save/load settings")
        save_load_menu.addAction("Save settings", self.save_config)
        save_load_menu.addAction("Load settings", self.load_config)
        menu.addAction("Export message", self.export_message)

        # ROTORS INDICATOR ====================================================

        logging.info("Generating rotor and reflector indicators...")
        self._rotors = _RotorsHandler(
            self,
            self.enigma_api.positions,
            self.enigma_api.generate_rotate_callback,
            self.enigma_api.rotate_reflector,
            enigma_api,
            self.refresh_gui,
            enigma_api.reflector_position,
        )

        # LIGHTBOARD FRAME ====================================================

        logging.info("Adding Lightboard...")
        self.lightboard = Lightboard(self, self.enigma_api.charset)

        # INPUT OUTPUT FOR ENCRYPTION/DECRYPTION ==============================

        logging.info("Adding I/O textboxes...")
        self.o_textbox = _OutputTextBox(
            self, self.lightboard.light_up, enigma_api.letter_group
        )
        self.i_textbox = _InputTextBox(
            self,
            enigma_api.encrypt,
            self.o_textbox.insert,
            self.o_textbox,
            self._rotors.set_positions,
            enigma_api.letter_group,
            enigma_api.revert_by,
            enigma_api.buffer_full,
            enigma_api.data()["charset"]
        )

        # PLUGBOARD BUTTONS ===================================================

        logging.info("Adding Plugboard button")
        self.plug_button = QPushButton("Plugboard")
        self.plug_button.setToolTip("Edit plugboard letter pairs")
        self.plug_button.clicked.connect(self.get_pairs)

        # SHOW WIDGETS ========================================================

        logging.info("Showing all widgets...")
        main_layout.addWidget(menu, alignment=Qt.AlignTop)
        main_layout.addWidget(self._rotors, alignment=Qt.AlignBottom)
        main_layout.addWidget(self.lightboard)
        main_layout.addWidget(
            QLabel("INPUT", self, styleSheet="font-size: 20px"),
            alignment=Qt.AlignCenter,
        )
        main_layout.addWidget(self.i_textbox)
        main_layout.addWidget(
            QLabel("OUTPUT", self, styleSheet="font-size: 20px"),
            alignment=Qt.AlignCenter,
        )
        main_layout.addWidget(self.o_textbox)
        main_layout.addWidget(self.plug_button)

        self.refresh_gui()
        self.show()

    def get_pairs(self):
        """Opens the plugboard menu"""
        logging.info("Opening Plugboard menu...")
        old_pairs = self.enigma_api.plug_pairs()

        plugboard = PlugboardDialog(self, self.enigma_api)
        plugboard.exec()

        logging.info("Closing plugboard...")

        new_pairs = self.enigma_api.plug_pairs()
        if old_pairs != new_pairs:
            logging.info('New plug pairs set to "%s"' % str(new_pairs))
        else:
            logging.info("No changes to plug pairs...")

        del plugboard

    def refresh_gui(self):
        """Refreshes main window GUI based on new EnigmaAPI settings"""
        logging.info("Refreshing GUI components...")
        self.setWindowTitle(self.enigma_api.model())
        self.i_textbox.clear()
        self.i_textbox.set_charset(self.enigma_api.data()["charset"])

        if self.enigma_api.data()["plugboard"]:  # If current model has a plugboard
            logging.info("Showing Plugboard button...")
            self.plug_button.show()
        else:
            logging.info("Hiding Plugboard button...")
            self.plug_button.hide()

        # Arrange lightbulbs to new layout
        self.lightboard.regenerate_bulbs(self.enigma_api.data()["layout"])

    def load_config(self):
        """Loads EnigmaAPI settings from config file and refershes GUI"""
        dialog = QFileDialog(self)
        filename = dialog.getOpenFileName(
            self, "Load settings", QDir.homePath(), "Enigma config (*.json)"
        )[0]

        if filename:
            try:
                self.enigma_api.load_from(filename)
                logging.info('Successfully loaded config from file "%s"' % filename)
            except (FileNotFoundError, JSONDecodeError) as e:
                QMessageBox.critical(
                    self, "Load config", "Error retrieving data from "
                          "selected file!\nError message:\n\n %s" % repr(e)
                )
                logging.error('Failed to load config from file "%s"' % filename, exc_info=True)
                return
            except Exception as e:
                QMessageBox.critical(self, "Load config", "Following error occured during "
                                           "applying loaded settings:\n%s" % repr(e))
                logging.error("Unable to load config from file, keeping old settings...", exc_info=True)
                return

            # Refresh gui after loading setings
            self._rotors.generate_rotors()
            self.i_textbox.blockSignals(True)
            self.refresh_gui()
            self.i_textbox.blockSignals(False)
            self._rotors.set_positions()
            logging.info('Checkpoint set to "%s"' % str(self.enigma_api.positions()))
            self.enigma_api.set_checkpoint()
        else:
            logging.info("No load file selected...")

    def save_config(self):
        """Collects data from EnigmaAPI and saves it to config"""
        dialog = QFileDialog(self)
        dialog.setDefaultSuffix("json")
        filename = dialog.getSaveFileName(
            self, "Save settings", QDir.homePath(), "Enigma config (*.json)"
        )[0]

        # To prevent from saving files without a file extension...
        if not findall(r"\.json$", filename):
            filename += ".json"
            logging.info(".json file extension for save file not found, adding...")

        if filename:
            self.enigma_api.save_to(filename)
        else:
            logging.info("No save file selected...")

    def export_message(self):
        """Opens a dialog to get the save location, exports current Enigma
        settings and encrypted message to the file"""
        dialog = QFileDialog(self)
        filename = dialog.getSaveFileName(
            self, "Save enigma message", QDir.homePath(), "*.txt"
        )[0]

        if not findall(r"\.txt$", filename):
            filename += ".txt"
            logging.info(".txt file extension for save file not found, adding...")

        if filename:
            logging.info('Exporing message to "%s"...' % filename)
            with open(filename, "w") as f:
                message = "\n".join(wrap(self.o_textbox.text(), 29))
                f.write("%s\n%s\n" % (str(self.enigma_api), message))


class Lightboard(QFrame):
    def __init__(self, master, charset_plug):
        """Creates a "board" representing Enigma light bulbs and allows their
        control
        """
        super().__init__(master)

        # BASIC QT SETTINGS  ==================================================

        self.lb_layout = QVBoxLayout(self)

        # ATTRIBUTES ==========================================================

        self._charset_plug = charset_plug
        self._lightbulbs = {}
        self._base_style = (
            "QLabel{background-color: black; color: %s; font-weight: bold;"
            "border-radius: 20px; font-size: 25px; text-align: center;}"
        )

        # CONSTRUCT LIGHTBOARD ================================================

        self.rows = []

        self.regenerate_bulbs(default_layout)

    def regenerate_bulbs(self, layout):
        self.clear_bulbs()
        for row in layout:
            if row:
                row_frame = QFrame(self)
                row_layout = QHBoxLayout(row_frame)
                row_layout.setAlignment(Qt.AlignCenter)
                row_layout.setSpacing(10)
                self.rows.append(row_frame)

                for letter in row:
                    ltr = self._charset_plug()[letter]
                    label = QLabel(ltr)
                    label.setFixedSize(40, 40)
                    label.setAlignment(Qt.AlignCenter)

                    self._lightbulbs[ltr] = label
                    row_layout.addWidget(label, Qt.AlignCenter)

                self.lb_layout.addWidget(row_frame)

        self.power_off()

    def clear_bulbs(self):
        for bulb in self._lightbulbs.values():
            bulb.deleteLater()
            del bulb
        self._lightbulbs = {}

        while self.rows:
            row = self.rows.pop() 
            row.deleteLater()
            del row

    def power_off(self):
        """
        Turns all lightbulbs black
        """
        for bulb in self._lightbulbs.values():
            bulb.setStyleSheet(self._base_style % "gray")

    def light_up(self, character):
        """
        Lights up character on the lightboard, only powers off if letter isn't
        not found
        :param character: {char} character to light up
        """
        self.power_off()

        if character in self._lightbulbs:
            self._lightbulbs[character].setStyleSheet(self._base_style % "yellow")


class _RotorsHandler(QFrame):
    def __init__(
        self,
        master,
        position_plug,
        rotate_plug,
        rotate_ref_plug,
        enigma_api,
        label_plug,
        reflector_pos_plug,
    ):
        """  # TODO: Missing comments
        :param master: {Qt} Master qt object
        :param position_plug: {callable} Callable method for getting rotor
                                         positions
        :param rotate_plug: {callable} Temporary callable for getting
                                       rotor offset handlers
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ==================================================

        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._layout = QHBoxLayout(self)
        self._layout.setAlignment(Qt.AlignCenter)
        self._rotor_layout = QHBoxLayout()
        self._rotor_indicators = []
        self._reflector_indicator = None

        # ATTRIBUTES ==========================================================

        self.enigma_api = enigma_api
        self._rotate_plug = rotate_plug
        self._position_plug = position_plug
        self._label_plug = label_plug
        self._rotate_ref_plug = rotate_ref_plug
        self._reflector_pos_plug = reflector_pos_plug

        # SETTINGS ICON =======================================================

        self.settings_button = QPushButton(QIcon(base_dir + "settings.png"), "", self)
        self.settings_button.setIconSize(QSize(50, 50))
        self.settings_button.setToolTip("Edit Enigma rotor and reflector settings")
        self.settings_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.settings_button.clicked.connect(self.open_settings)

        # GENERATE ROTORS AND REFLECTOR =======================================

        self.ukwd_indicator = QLabel("D")
        self.ukwd_indicator.setStyleSheet(
            "QLabel{font-size: 20px; text-align: center; background-color: white; color: red}"
        )
        self.ukwd_indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.ukwd_indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.ukwd_indicator.setLineWidth(2)
        self.ukwd_indicator.setFixedSize(40, 40)
        self.ukwd_indicator.hide()

        self._reflector_indicator = _RotorHandler(
            self,
            self._rotate_ref_plug(1, True),
            self._rotate_ref_plug(-1, True),
            self.set_positions,
        )
        self._reflector_indicator.setToolTip("Reflector position indicator")
        self._reflector_indicator.hide()

        self._left_spacer = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self._right_spacer = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding
        )

        self.generate_rotors()
        self.set_positions()

    def generate_rotors(self):
        """
        Regenerates rotor and reflector views (with position indicators and
        and buttons to rotate them
        """
        self._layout.removeItem(self._left_spacer)
        self._layout.removeItem(self._right_spacer)
        self._layout.removeWidget(self.settings_button)
        self._layout.removeWidget(self.ukwd_indicator)
        self.ukwd_indicator.hide()
        self._reflector_indicator.hide()
        self._layout.removeWidget(self._reflector_indicator)
        self._reflector_indicator.hide()

        for indicator in self._rotor_indicators:
            indicator.deleteLater()

        self._layout.addItem(self._left_spacer)

        self._rotor_indicators = []

        if self.enigma_api.reflector() == "UKW-D":
            logging.info("UKW-D reflector detected, showing indicator...")
            self._layout.addWidget(self.ukwd_indicator)
            self.ukwd_indicator.show()
        elif self.enigma_api.reflector_rotatable():
            logging.info("Rotatable reflector detected, showing indicator...")
            self._layout.addWidget(self._reflector_indicator)
            self._reflector_indicator.show()

        # Create
        for i in range(len(self._position_plug())):  # Rotor controls
            indicator = _RotorHandler(
                self,
                self._rotate_plug(i, 1),
                self._rotate_plug(i, -1),
                self.set_positions,
            )
            self._layout.addWidget(indicator, alignment=Qt.AlignLeft)
            self._rotor_indicators.append(indicator)

        self._layout.addItem(self._right_spacer)
        self._layout.addWidget(self.settings_button)

    def open_settings(self):
        """
        Opens settings and reloads indicators
        """
        logging.info("Opening settings menu...")
        old_cfg = self.enigma_api.get_config()
        settings = Settings(self, self.enigma_api)
        settings.exec()  # Exec gives focus to top window, unlike .show
        if old_cfg != self.enigma_api.get_config():
            logging.info("Settings changed, reloading GUI...")
            del settings
            self.generate_rotors()
            self._label_plug()
            self.set_positions()
        else:
            logging.info("No changes to settings made...")

    def set_positions(self):
        """
        Refreshes position indicators to show new positions from EnigmaAPI
        """
        if (
            self.enigma_api.reflector_rotatable()
            and self.enigma_api.reflector() != "UKW-D"
        ):
            logging.info('Reflector indicator set to position "%s"' % self._reflector_pos_plug())
            self._reflector_indicator.set(self._reflector_pos_plug())

        logging.info('Rotor indicators set to positions "%s"' % str(self._position_plug()))
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

        # QT WINDOW SETTINGS ==================================================

        self._layout = QVBoxLayout(self)

        # SAVE ATTRIBUTES =====================================================

        self.plus_plug = plus_plug
        self.minus_plug = minus_plug
        self.set_positions = set_pos_plug

        # ROTATE FORWARD ======================================================

        self.position_plus = QPushButton("+", self)
        self.position_plus.clicked.connect(self.increment)
        self.position_plus.setFixedSize(40, 40)
        self.position_plus.setToolTip("Rotates rotor forwards by one place")

        # POSITION INDICATOR ==================================================

        self._indicator = QLabel("A", self)
        self._indicator.setStyleSheet(
            "QLabel{font-size: 20px; text-align: center;"
            "background-color: white}"
        )
        self._indicator.setFixedSize(40, 40)
        self._indicator.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self._indicator.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self._indicator.setLineWidth(2)

        # ROTATE FORWARD ======================================================

        self.position_minus = QPushButton("-", self)
        self.position_minus.setFixedSize(40, 40)
        self.position_minus.clicked.connect(self.decrement)
        self.position_minus.setToolTip("Rotates rotors backwards by one place")

        # SHOW WIDGETS ========================================================

        self._layout.addWidget(self.position_plus, alignment=Qt.AlignCenter)
        self._layout.addWidget(self._indicator, alignment=Qt.AlignCenter)
        self._layout.addWidget(self.position_minus, alignment=Qt.AlignCenter)

    def set(self, position):
        """
        Sets indicator position to specified text
        """
        self._indicator.setText(position)

    def increment(self):
        """
        Increments rotor position by one (1)
        """
        self.plus_plug()
        self.set_positions()

    def decrement(self):
        """
        Decrements rotor position by one (-1)
        """
        self.minus_plug()
        self.set_positions()


def letter_groups(text, group_size=5):
    """
    Formats letter into blocks according to group size
    :param text: {str} Text to "blockify"
    :param group_size: {int} Size of blocks
    """
    output = ""
    i = 0
    for letter in text:
        if i == group_size:
            i = 0
            output += " "
        output += letter
        i += 1
    return output


class _InputTextBox(QPlainTextEdit):
    def __init__(
        self,
        master,
        encrypt_plug,
        output_plug,
        output_textbox,
        refresh_plug,
        letter_group_plug,
        revert_pos,
        overflow_plug,
        charset
    ):
        """
        Handles user input and sends it to the output textbox
        :param master: {QWidget} Parent Qt object
        :param encrypt_plug: {callable} A callable that accepts one letter
                                        and returns one letter, should provide
                                        encryption
        :param output_plug: {callable} Accepts text that is to be displayed
        :param output_textbox: {callable} Output textbox object
        :param refresh_plug: {callable} Refreshes displayed rotor positions
                                        a rotor positions
        :param letter_group_plug: {callable} Formats input text into blocks of
                                             n letters
        :param revert_pos: {callable} Reverts Enigma rotor position when the
                                      text gets shorter
        :param overflow_plug: {callable} Checks if the position buffer is overflowing
        """
        super().__init__(master)

        # QT WIDGET SETTINGS ==================================================

        self.setPlaceholderText("Type your message here")
        self.textChanged.connect(self.input_detected)
        self.setStyleSheet("background-color: white;")

        # FONT ================================================================

        font = QFont("Monospace", 12)
        self.setFont(font)

        # PLUGS ===============================================================

        self.encrypt_plug = encrypt_plug
        self.output_plug = output_plug
        self.sync_plug = output_textbox.sync_length
        self.other_scrollbar = output_textbox.verticalScrollBar()
        self.output_textbox = output_textbox
        self.refresh_plug = refresh_plug
        self.letter_group_plug = letter_group_plug
        self._revert_pos = revert_pos
        self.overflow_plug = overflow_plug
        self.charset = "[^%s]+" % charset

        # SCROLLBAR SYNC ======================================================

        self.verticalScrollBar().valueChanged.connect(self.sync_scroll)
        self.other_scrollbar.valueChanged.connect(lambda new_val: self.sync_scroll(new_val, True))

        # HIGHLIGHTER =========================================================

        output_textbox.selectionChanged.connect(self.select_block)
        self.selectionChanged.connect(lambda: self.select_block(True))

        # ATTRIBUTES ==========================================================

        self.last_len = 0
        self._revert_pos = revert_pos
    
    def set_charset(self, charset):
        self.charset = "[^%s]+" % charset

    def select_block(self, this=False):
        """
        Synchronizes selection blocks between two menus
        """
        if this:
            cursor = self.textCursor()
            start, end = cursor.selectionStart(), cursor.selectionEnd()
            new_cursor = self.output_textbox.textCursor()
            new_cursor.setPosition(start)
            new_cursor.setPosition(end, QTextCursor.KeepAnchor)
            self.output_textbox.blockSignals(True)
            self.output_textbox.setTextCursor(new_cursor)
            self.output_textbox.blockSignals(False)
        else:
            cursor = self.output_textbox.textCursor()
            start, end = cursor.selectionStart(), cursor.selectionEnd()
            new_cursor = self.textCursor()
            new_cursor.setPosition(start)
            new_cursor.setPosition(end, QTextCursor.KeepAnchor)
            self.blockSignals(True)
            self.setTextCursor(new_cursor)
            self.blockSignals(False)

    def input_detected(self):
        """
        Encrypts newly typed/inserted text and outputs it to the output textbox
        """
        text = sub(self.charset, "", self.toPlainText().upper())

        new_len = len(text)
        diff = self.last_len - new_len


        if diff <= -10000:  # If insertion greater than 10 000 chars
            logging.warning('Blocked attempt to insert %d characters...' % abs(diff))
            QMessageBox.critical(
                self, "Input too long", "Inserting more than 10000 characters at a time is disallowed!"
            )
            text = text[:self.last_len]
            self.sync_plug(self.last_len)
        elif diff != 0:  # If anything changed
            if diff < 0:  # If text longer than before
                encrypted = "".join(map(self.encrypt_plug, text[diff:]))

                if len(encrypted) <= 30:
                    logging.info('Buffer longer by %d, new encrypted text "%s"' % (abs(diff), encrypted))
                else:
                    logging.info('Buffer longer by %d, new encrypted text "%s..."' % (abs(diff), encrypted[:30]))

                self.output_plug(encrypted)

                if self.overflow_plug():
                    logging.warning("Position buffer is full, trimming...")
            elif diff > 0:  # If text shorter than before
                logging.info("Buffer shorter by %d, trimming and reverting positions..." % abs(diff))

                self.sync_plug(new_len)
                self._revert_pos(diff)

            self.refresh_plug()
            self.last_len = new_len
        else:
            logging.info("No changes to buffer made...")

        if len(text) == 0:
            logging.info("Text buffer now empty...")

        self.set_text(text)

    def sync_scroll(self, new_val, other=False):
        if other:
            self.other_scrollbar.blockSignals(True)
            self.verticalScrollBar().setValue(new_val)
            self.other_scrollbar.blockSignals(False)
        else:
            self.verticalScrollBar().blockSignals(True)
            self.other_scrollbar.setValue(new_val)
            self.verticalScrollBar().blockSignals(False)

    def set_text(self, text):
        self.blockSignals(True)  # Blocks programatical edits to the widget
        self.setPlainText(letter_groups(text, self.letter_group_plug()))
        self.moveCursor(QTextCursor.End)
        self.blockSignals(False)


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
        self.setStyleSheet("background-color: white;")

        # FONT ================================================================

        font = QFont("Monospace", 12)
        self.setFont(font)

    def sync_length(self, length):
        """
        Sets widget length to the desired length
        :param length: {int} new length of the displayed text
        """
        self.light_up_plug("")
        text = letter_groups(
            self.toPlainText().replace(" ", "")[:length], self.letter_group_plug()
        )

        self.setPlainText(text)
        self.moveCursor(QTextCursor.End)
        try:
            self.light_up_plug(self.toPlainText()[-1])
        except IndexError:
            pass

    def insert(self, text):
        """
        Appends text into the textbox
        :param text: {char} Letter to be appended
        """
        text = self.toPlainText().replace(" ", "") + text
        self.setPlainText(letter_groups(text, self.letter_group_plug()))
        self.light_up_plug(text[-1])
        self.moveCursor(QTextCursor.End)

    def text(self):
        """
        Returns currently displayed text
        """
        return self.toPlainText()
