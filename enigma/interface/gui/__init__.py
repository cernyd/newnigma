from PySide2.QtWidgets import *
from PySide2.QtCore import QUrl, QSize, Qt, QDir
from PySide2.QtGui import QIcon, QFont, QPixmap, QTextCursor, QDesktopServices
from string import ascii_uppercase as alphabet
from enigma.utils.cfg_handler import save_config, load_config
from enigma import contains

labels = [
    "A-01",
    "B-02",
    "C-03",
    "D-04",
    "E-05",
    "F-06",
    "G-07",
    "H-08",
    "I-09",
    "J-10",
    "K-11",
    "L-12",
    "M-13",
    "N-14",
    "O-15",
    "P-16",
    "Q-17",
    "R-18",
    "S-19",
    "T-20",
    "U-21",
    "V-22",
    "W-23",
    "X-24",
    "Y-25",
    "Z-26",
]

# For the GUI plug board
layout = [
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
every part of the army
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
Naval version featuring 4 rotors, the last rotor is stationary.
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
Enigma I machines captured and used by the norwegian secret service after 1945.
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
used commercially and by the police
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
Commercially used Enigma model
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
Improved Enigma D, 'K' probably stands for 'Komerziell'
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
Rewired version of the Enigma K used by the german railway.
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
Rewired version of the Enigma K used by the Japanese army
"""


stylesheet = 'font-family: "Courier New", Courier, monospace'


view_data = {
    "Enigma1": {"description": _enigma1, "img": base_dir + "enigma1.jpg"},
    "EnigmaM3": {"description": _enigmam3, "img": base_dir + "enigmam3.jpg"},
    "EnigmaM4": {"description": _enigmam4, "img": base_dir + "enigmam4.jpg"},
    "Norenigma": {"description": _norenigma, "img": base_dir + "enigma1.jpg"},
    "EnigmaG": {"description": _enigmag, "img": base_dir + "/enigmag.jpg"},
    "EnigmaD": {
        "description": _enigmad,
        "img": base_dir + "enigmad.jpg",
    },  # UKW CAN ROTATE
    "EnigmaK": {"description": _enigmak, "img": base_dir + "enigmak.jpg"},
    "SwissK": {"description": _swissk, "img": base_dir + "swissk.png"},
    "Railway": {"description": _railway, "img": base_dir + "enigmak.jpg"},
    "Tirpitz": {"description": _tirpitz, "img": base_dir + "tirpitz.jpg"},
}


class AbstractPlugboard(QDialog):
    def __init__(self, master, enigma_api, title):
        super().__init__(master)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(title)
        self.enigma_api = enigma_api

        self.pairs = {}  # TODO: Duplicate
        self.plugs = {}
        self.banned = []

    def _pairs(self):  # TODO: Duplicate
        """
        Returns all selected wiring pairs
        """
        pairs = []
        for pair in self.pairs.items():
            if not contains(pairs, pair) and all(pair):
                pairs.append(pair)

        return pairs

    def set_pairs(self, new_pairs=[]):
        if new_pairs:
            for pair in new_pairs:
                self.connect_sockets(*pair)
        else:
            for key in self.pairs:
                self.pairs[key] = None
            for plug in self.plugs.values():
                plug.set_text("")

    def storno(self):
        """
        Clears all selected pairs and closes the window
        """
        self.pairs = {}
        self.close()

    def connect_sockets(self, socket, other_socket):
        """
        Connects two sockets without unnecessary interaction of two sockets
        to avoid recursive event calls)
        """
        if not other_socket:
            other = self.pairs[socket]

            self.pairs[other] = None
            self.pairs[socket] = None
            self.plugs[socket].set_text("")
            self.plugs[other].set_text("")
        else:
            if other_socket in self.banned or not other_socket:
                self.plugs[socket].set_text("")
                return

            if self.pairs[other_socket]:
                self.plugs[socket].set_text("")
            elif socket == other_socket:
                self.plugs[socket].set_text("")
            else:
                self.pairs[socket] = other_socket
                self.pairs[other_socket] = socket
                self.plugs[socket].set_text(other_socket)
                self.plugs[other_socket].set_text(socket)


class Socket(QFrame):
    def __init__(self, master, letter, connect_plug, apply_plug):
        """
        One sockets with label and text entry
        :param master: Qt parent object
        :param letter: Letter to serve as the label
        :param connect_plug: calls parent to connect with the letter typed in
                             the entry box
        :param apply_plug: Refreshes the "Apply" button
        """
        super().__init__(master)

        # QT WINDOW SETTINGS ===================================================

        layout = QVBoxLayout(self)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

        # ATTRIBUTES ===========================================================

        self.connect_plug = connect_plug
        self.letter = letter
        self.apply_plug = apply_plug
        self.connected_to = None

        # ENTRY ================================================================

        label = QLabel(letter)
        label.setStyleSheet("font-size: 30px; text-align: center;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.entry = QLineEdit()
        self.entry.setMaxLength(1)
        self.entry.textChanged.connect(self.entry_event)
        self.entry.setFixedSize(40, 40)
        self.entry.setAlignment(Qt.AlignCenter)

        # SHOW WIDGETS

        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(self.entry, alignment=Qt.AlignCenter)

    def entry_event(self):
        """
        Responds to a event when something changes in the plug entry
        """
        self.apply_plug()

        text = self.entry.text().upper()
        if self.entry.isModified():  # Prevents recursive event calls
            if text:
                self.connect_plug(self.letter, text)
            else:
                self.connect_plug(self.letter, None)

    def set_text(self, letter):
        """
        Sets text to the plug entrybox and sets white (vacant) or black
        (occupied) background color
        :param letter: Sets text to the newly selected letter
        """
        if letter:
            self.entry.setStyleSheet("background-color: black; color: white;"
                                     "text-align: center;"
                                     "font-size: 30px;")
        else:
            self.entry.setStyleSheet("background-color: white; color: black;"
                                     "text-align: center; font-size: 30px;")
        self.entry.setText(letter)
