from PySide2.QtWidgets import *
from PySide2.QtCore import QUrl, QSize, Qt, QDir
from PySide2.QtGui import QIcon, QFont, QPixmap, QTextCursor, QDesktopServices
from enigma.utils.cfg_handler import save_config, load_config
from enigma.core.components import historical
from json import JSONDecodeError
import logging


labels = [
    "A-01", "B-02", "C-03", "D-04", "E-05", "F-06", "G-07", "H-08", "I-09", "J-10",
    "K-11", "L-12", "M-13", "N-14", "O-15", "P-16", "Q-17", "R-18", "S-19", "T-20",
    "U-21", "V-22", "W-23", "X-24", "Y-25", "Z-26"
]

# For the GUI plug board
default_layout = [
    [16, 22, 4, 17, 19, 25, 20, 8, 14],
    [0, 18, 3, 5, 6, 7, 9, 10],
    [15, 24, 23, 2, 21, 1, 13, 12, 11],
]

# Data for enigma settings model wiki


base_dir = "enigma/interface/gui/assets/icons/"


_enigma1 = """
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

_enigmam3 = """
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

_enigmam4 = """
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

_norenigma = """
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

_enigmag = """
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

_enigmad = """
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

_enigmak = """
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

_swissk = """
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

_railway = """
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

_tirpitz = """
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

_enigmakd = """
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

_enigmag111 = """
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

_enigmag260 = """
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

_enigmag312 = """
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

stylesheet = 'font-family: "Courier New", Courier, monospace'

view_data = {}
resources = {
    "Enigma I": {"description": _enigma1, "img": base_dir + "enigma1.jpg"},
    "Enigma M3": {"description": _enigmam3, "img": base_dir + "enigmam3.jpg"},
    "Enigma M4": {"description": _enigmam4, "img": base_dir + "enigmam4.jpg"},
    "Norenigma": {"description": _norenigma, "img": base_dir + "enigma1.jpg"},
    "Enigma G (A865)": {"description": _enigmag, "img": base_dir + "enigmag.jpg"},
    "Enigma G (G-111)": {"description": _enigmag111, "img": base_dir + "enigmag.jpg"},
    "Enigma G (G-260)": {"description": _enigmag260, "img": base_dir + "enigmag.jpg"},
    "Enigma G (G-312)": {"description": _enigmag312, "img": base_dir + "enigmag.jpg"},
    "Enigma D": {
        "description": _enigmad,
        "img": base_dir + "enigmad.jpg",
    },
    "Enigma K": {"description": _enigmak, "img": base_dir + "enigmak.jpg"},
    "Enigma KD": {"description": _enigmakd, "img": base_dir + "enigmak.jpg"},
    "Swiss K": {"description": _swissk, "img": base_dir + "swissk.png"},
    "Railway": {"description": _railway, "img": base_dir + "enigmak.jpg"},
    "Tirpitz": {"description": _tirpitz, "img": base_dir + "tirpitz.jpg"},
}


for model in historical:
    view_data[model] = resources.get(model, {
        "description": "<h1>%s</h1>\n<hr>\nNo description given" % model,
        "img": base_dir + "unknown.jpg"
    })


def load_mods(mod_cfg):  # TODO: Fully implement mod loader in the end
    for mod in mod_cfg:
        view_data = mod.get(['view_data'], {
            "description": "<h1>%s</h1>\n<hr>\nNo description given" % model,
            "img": base_dir + "unknown.jpg"
        })
        # config = mod.


class AbstractPlugboard(QDialog):
    def __init__(self, master, enigma_api, title):
        super().__init__(master)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(title)
        self.enigma_api = enigma_api

        self.old_pairs = {}
        self.plugs = {}
        self.banned = []
        self.uhr_enabled = False
        self.apply_plug = lambda: None

    def _pairs(self):  # TODO: Duplicate
        """
        Returns all selected wiring pairs
        """
        pairs = []
        for plug in self.plugs.values():
            marking = plug.marking
            if marking and "a" in marking:
                pairs.append((marking[0], plug.pair()))

        return [pair[1] for pair in sorted(pairs, key=lambda pair: pair[0])]

    def set_pairs(self, new_pairs=[]):
        self.clear_pairs()
        if new_pairs:
            logging.info('Setting wiring pairs to "%s"' % str(new_pairs))
            for pair in new_pairs:
                self.connect_sockets(*pair, False)
            self.old_pairs = self._pairs()

        self.apply_plug()

    def apply(self):
        self.old_pairs = self._pairs()
        self.close()

    def clear_pairs(self):
        logging.info("Clearing all wiring pairs...")
        for plug in self.plugs.values():
            self.connect_sockets(plug.letter, None, False)

        self.apply_plug()

    def storno(self):
        """
        Clears all selected pairs and closes the window
        """
        logging.info("Cancelling changes to wiring...")
        self.set_pairs(self.old_pairs)
        self.close()

    def connect_sockets(self, socket, other_socket, refresh=True):
        """
        Connects two sockets without unnecessary interaction of two sockets
        to avoid recursive event calls)
        """
        plug = self.plugs[socket]

        if not other_socket:  # Disconnect
            other = self.plugs[socket].connected_to
            plug.set_text(None)
            if other:
                self.plugs[other].set_text(None)
        else:
            # Check if letter is valid
            if other_socket in self.banned + [socket] or self.plugs[other_socket].pair() \
               or (len(self._pairs()) == 10 and self.uhr_enabled):
                plug.set_text("")
            else:  # Connects sockets
                plug_id = len(self._pairs()) + 1
                a_plug = (plug_id, "a")
                b_plug = (plug_id, "b")

                if self.uhr_enabled:
                    plug.set_text(other_socket, False, a_plug, True)
                    self.plugs[other_socket].set_text(socket, False, b_plug, True)
                else:
                    plug.set_text(other_socket, False, a_plug)
                    self.plugs[other_socket].set_text(socket, False, b_plug)

        if refresh:
            self.apply_plug()


class Socket(QFrame):
    def __init__(self, master, letter, connect_plug):
        """
        One sockets with label and text entry
        :param master: Qt parent object
        :param letter: Letter to serve as the label
        :param connect_plug: calls parent to connect with the letter typed in
                             the entry box
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
        """
        Returns currently wired pair.
        """
        if self.connected_to:
            return self.letter + self.connected_to
        else:
            return None

    def entry_event(self):
        """
        Responds to a event when something changes in the plug entry
        """
        letter = self.entry.text().upper()
        if letter not in alphabet:
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
        """
        stylesheet = "background-color: %s; color: %s; text-align: center; font-size: 30px;"

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

            self.setToolTip(str(marking[0])+marking[1])

        self.entry.setStyleSheet(stylesheet % color)
        self.entry.setText(letter)
        self.connected_to = letter

        if block_event:
            self.entry.blockSignals(False)
