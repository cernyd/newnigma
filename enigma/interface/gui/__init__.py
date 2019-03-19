"""Shared abstract objects (Plugboard and Socket) and wiki data."""
import logging

from PySide2.QtCore import Qt  # pylint: disable=no-name-in-module
from PySide2.QtWidgets import QVBoxLayout  # pylint: disable=no-name-in-module;
from PySide2.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QSizePolicy

from enigma.core.components import HISTORICAL

LABELS = [
    "A-01", "B-02", "C-03", "D-04", "E-05", "F-06", "G-07",
    "H-08", "I-09", "J-10", "K-11", "L-12", "M-13", "N-14",
    "O-15", "P-16", "Q-17", "R-18", "S-19", "T-20", "U-21",
    "V-22", "W-23", "X-24", "Y-25", "Z-26"
]

# Data for Enigma settings model wiki
BASE_DIR = "enigma/interface/gui/assets/icons/"


_ENIGMA1 = """
<h1>Enigma I</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: 20 000</li>
<li>Used by: Heer, Luftwaffe, Kriegsmarine</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
The Enigma M1 model was used primarily before the second world war
"""

_ENIGMAM3 = """
<h1>Enigma M3 (M1, M2, M3)</h1>
<hr>
<ul>
<li>Developed in: 1934</li>
<li>Number produced: 611 M1 units, 890 M2 units, 800 M3 units</li>
<li>Used by: Heer, Luftwaffe, Kriegsmarine</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
Backward compatible with Enigma I, but featured different rotors for
every part of the army. Enigma M1, M2 and M3 variants are practically
identical (aside from some minor manufacturing differences).
"""

_ENIGMAM4 = """
<h1>Enigma M4</h1>
<hr>
<ul>
<li>Developed in: 1942</li>
<li>Number produced: 1500 (estimated)</li>
<li>Used by: Kriegsmarine</li>
<li>Rotor count: 4</li>
<li>Features: Plugboard, thin reflectors</li>
</ul>
<hr>
Naval version featuring 4 rotors, the last rotor is "thin" and stationary.
Due to the increased number of rotors is more secure than 3 rotor variants.
"""

_NORENIGMA = """
<h1>Norenigma/Norway Enigma</h1>
<hr>
<ul>
<li>Developed in: -</li>
<li>Number produced: ?</li>
<li>Used by: Norwegian Police Security Service (Overvaakingspolitiet)</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
Enigma I machines captured and used by the Norwegian secret service after 1945.
Used custom rotor wiring.
"""

_ENIGMAG = """
<h1>Enigma G</h1>
<hr>
<ul>
<li>Developed in: 1931</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use, Abwehr, Sicherheitsdienst</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, cog driven rotors</li>
</ul>
<hr>
A compact Enigma model that featured a different rotor turning mechanism,
used commercially and by the police. Models A865, G111, G260 and G312 are
examples of rewired Enigma G.
"""

_ENIGMAD = """
<h1>Enigma D</h1>
<hr>
<ul>
<li>Developed in: 1926</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Commercially used Enigma model with rotatable reflector.
Predecessor of Enigma K.
"""

_ENIGMAK = """
<h1>Enigma K</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use, Swiss army, Italian navy, Reichsbahn, Spanish civil war</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Improved Enigma D, 'K' probably stands for 'Komerziell'. It is
the basis for Swiss K, Railway Enigma and Tirpitz.
"""

_SWISSK = """
<h1>Swiss Enigma K</h1>
<hr>
<ul>
<li>Developed in: 1939</li>
<li>Number produced: 65 (?)</li>
<li>Used by: Swiss army</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, modified wheel stepping, extra lamp board, power supply with transformer</li>
</ul>
<hr>
Used by the Swiss army, the extra lamp panel was used by a person who wrote down the letters.
"""

_RAILWAY = """
<h1>Railway</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: ?</li>
<li>Used by: Reichsbanh</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Rewired version of the Enigma K used by the German railway. Turnover
notches are swapped.
"""

_TIRPITZ = """
<h1>Tirpitz</h1>
<hr>
<ul>
<li>Developed in: 1942</li>
<li>Number produced: ?</li>
<li>Used by: Communication between Germany and Japan</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Version of the Enigma K used by the Japanese army, all rotors,
reflectors and stator are rewired.
"""

_ENIGMAKD = """
<h1>Enigma KD</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: -</li>
<li>Used by: Mil Amt (department of German intelligence service)</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Standard Enigma K but has differently wired wheels and rewirable reflector
UKW-D, originally found wiring is included, but it was probably frequently
rewired.
"""

_ENIGMA111 = """
<h1>Enigma G (G-111)</h1>
<hr>
<ul>
<li>Developed in: 1931</li>
<li>Number produced: -</li>
<li>Used by: Unknown</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, cog driven rotors</li>
</ul>
<hr>
Rewired Enigma G with serial number G-111. Surfaced in 2009 at an
auction in Munich.
"""

_ENIGMAG260 = """
<h1>Enigma G (G-260)</h1>
<hr>
<ul>
<li>Developed in: 1931</li>
<li>Number produced: -</li>
<li>Used by: Johann Siegfried Becker</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, cog driven rotors</li>
</ul>
<hr>
Enigma G machine with serial number G-260 found in possession of
Johann Siegfried Becker, a German spy, when he was arrested in Argentine.
"""

_ENIGMAG312 = """
<h1>Enigma G (G-312)</h1>
<hr>
<ul>
<li>Developed in: 1931</li>
<li>Number produced: -</li>
<li>Used by: Abwehr (?)</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, cog driven rotors</li>
</ul>
<hr>
Enigma G machine with serial number G-312, likely used by the Abwehr,
completely rewired.
"""

STYLESHEET = 'font-family: "Courier New", Courier, monospace'

VIEW_DATA = {}
RESOURCES = {
    "Enigma I": {"description": _ENIGMA1, "img": BASE_DIR + "enigma1.jpg"},
    "Enigma M3": {"description": _ENIGMAM3, "img": BASE_DIR + "enigmam3.jpg"},
    "Enigma M4": {"description": _ENIGMAM4, "img": BASE_DIR + "enigmam4.jpg"},
    "Norenigma": {"description": _NORENIGMA, "img": BASE_DIR + "enigma1.jpg"},
    "Enigma G (A865)": {"description": _ENIGMAG, "img": BASE_DIR + "enigmag.jpg"},
    "Enigma G (G-111)": {"description": _ENIGMA111, "img": BASE_DIR + "enigmag.jpg"},
    "Enigma G (G-260)": {"description": _ENIGMAG260, "img": BASE_DIR + "enigmag.jpg"},
    "Enigma G (G-312)": {"description": _ENIGMAG312, "img": BASE_DIR + "enigmag.jpg"},
    "Enigma D": {"description": _ENIGMAD, "img": BASE_DIR + "enigmad.jpg"},
    "Enigma K": {"description": _ENIGMAK, "img": BASE_DIR + "enigmak.jpg"},
    "Enigma KD": {"description": _ENIGMAKD, "img": BASE_DIR + "enigmak.jpg"},
    "Swiss K": {"description": _SWISSK, "img": BASE_DIR + "swissk.png"},
    "Railway": {"description": _RAILWAY, "img": BASE_DIR + "enigmak.jpg"},
    "Tirpitz": {"description": _TIRPITZ, "img": BASE_DIR + "tirpitz.jpg"},
}


def load_views(configs):
    """Loads dictionary objects to VIEW_DATA in order to be selectable
    in the GUI.
    :param configs: {dict} Dictionary of configurations to load
    """
    for model, data in configs.items():
        description = data.get("description", "No description given")
        VIEW_DATA[model] = RESOURCES.get(
            model,
            {
                "description": "<h1>%s</h1>\n<hr>\n%s" % (model, description),
                "img": BASE_DIR + "unknown.jpg",
            }
        )


load_views(HISTORICAL)


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


class _AbstractPlugboard(QDialog):
    """Abstract object with features shared by all 'pair connect' windows"""

    def __init__(self, master, enigma_api, title):
        super().__init__(master)

        self._main_layout = QVBoxLayout()
        self.setLayout(self._main_layout)
        self.setWindowTitle(title)
        self._enigma_api = enigma_api

        self._old_pairs = {}
        self._plugs = {}
        self._banned = []
        self._uhr_enabled = False
        self._apply_plug = lambda: None

    def pairs(self):
        """Returns all selected wiring pairs
        """
        pairs = []
        for plug in self._plugs.values():
            marking = plug.marking
            if marking and "a" in marking:
                pairs.append((marking[0], plug.pair()))

        return [pair[1] for pair in sorted(pairs, key=lambda pair: pair[0])]

    def set_pairs(self, new_pairs=None):
        """Sets pairs to new pairs and connects corresponding sockets
        :param new_pairs: {[str, str, str, ...]}
        """
        self.clear_pairs()
        if new_pairs:
            logging.info('Setting wiring pairs to "%s"', str(new_pairs))
            for pair in new_pairs:
                self.connect_sockets(*pair, False)
            self._old_pairs = self.pairs()

        self._apply_plug()

    def apply(self):
        """Sets current pairs to the ones that will be collected, closes window
        """
        self._old_pairs = self.pairs()
        self.close()

    def clear_pairs(self):
        """Clears all pairs and sockets"""
        logging.info("Clearing all wiring pairs...")
        for plug in self._plugs.values():
            self.connect_sockets(plug.letter, None, False)

        self._apply_plug()

    def storno(self):
        """Clears all selected pairs and closes the window"""
        logging.info("Cancelling changes to wiring...")
        self.set_pairs(self._old_pairs)
        self.close()

    def connect_sockets(self, socket, other_socket, refresh=True):
        """Connects two sockets without unnecessary interaction of two sockets
        to avoid recursive event calls)
        :param socket: {char} Letter for the calling sockets
        :param other_socket: {char} letter for the other socket, disconnects the
        first parameter socket if None
        :param refresh: {bool} Whether or not the GUI should
                               be refreshed after making changes
        """
        plug = self._plugs[socket]

        if not other_socket:  # Disconnect
            other = self._plugs[socket].connected_to
            plug.set_text(None)
            if other:
                self._plugs[other].set_text(None)
        else:
            # Check if letter is valid
            socket_unavailable = other_socket in self._banned + [socket]
            socket_used = self._plugs[other_socket].pair()
            uhr_full = len(self.pairs()) == 10 and self._uhr_enabled

            if socket_unavailable or socket_used or uhr_full:
                plug.set_text("")
            else:  # Connects sockets
                plug_id = len(self.pairs()) + 1
                a_plug = (plug_id, "a")
                b_plug = (plug_id, "b")

                if self._uhr_enabled:
                    plug.set_text(other_socket, False, a_plug, True)
                    self._plugs[other_socket].set_text(socket, False, b_plug, True)
                else:
                    plug.set_text(other_socket, False, a_plug)
                    self._plugs[other_socket].set_text(socket, False, b_plug)

        if refresh:
            self._apply_plug()


class Socket(QFrame):
    """One socket with label and text entry"""

    def __init__(self, master, letter, connect_plug, charset):
        """
        :param master: Qt parent object
        :param letter: Letter to serve as the label
        :param connect_plug: calls parent to connect with the letter typed in
                             the entry box
        :param charset: {str} Allowed letters
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # ATTRIBUTES ===========================================================

        self.connect_plug = connect_plug
        self.letter = letter
        self.connected_to = None
        self.marking = None
        self.charset = charset

        # ENTRY ================================================================

        label = QLabel(letter)
        label.setStyleSheet("font-size: 30px; text-align: center;")
        self.entry = QLineEdit()
        self.entry.setMaxLength(1)
        self.entry.textChanged.connect(self.entry_event)
        self.entry.setFixedSize(40, 40)
        self.entry.setAlignment(Qt.AlignCenter)

        # SHOW WIDGETS

        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)

    def pair(self):
        """Returns currently wired pair."""
        if self.connected_to:
            return self.letter + self.connected_to
        return None

    def entry_event(self):
        """Responds to a event when something changes in the plug entry"""
        letter = self.entry.text().upper()
        if letter not in self.charset:
            self.set_text("", True)
        elif self.entry.isModified():  # Prevents recursive event calls
            if letter:
                self.connect_plug(self.letter, letter)
            else:
                self.connect_plug(self.letter, None)

    def set_text(self, letter, block_event=False, marking=None, uhr=False):
        """
        Sets text to the plug entrybox and sets white (vacant) or black
        (occupied) background color
        :param letter: Sets text to the newly selected letter
        :param block_event: {bool} Starts blocking Qt signals if True
        :param marking: {str} Uhr marking (like 1a, 3b, ...)
        :param uhr: {bool} Colors sockets differently when True (when Uhr connected)
        """
        stylesheet = (
            "background-color: %s; color: %s; text-align: center; font-size: 30px;"
        )

        if block_event:
            self.entry.blockSignals(True)

        self.setToolTip(None)

        if letter:
            color = ("black", "white")
            self.marking = marking
        else:
            color = ("white", "black")
            self.marking = None

        if uhr:
            if "a" in marking:
                color = ("red", "white")
            else:
                color = ("gray", "white")

            self.setToolTip(str(marking[0]) + marking[1])

        self.entry.setStyleSheet(stylesheet % color)
        self.entry.setText(letter)
        self.connected_to = letter

        if block_event:
            self.entry.blockSignals(False)
