from enigma import contains
from enigma.core.extensions import Uhr

# Stators
ETW = {"wiring": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
ETW_QWERTZ = {"wiring": "QWERTZUIOASDFGHJKPYXCVBNML"}

# Rotors
I = {"label": "I", "wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": "Q"}
II = {"label": "II", "wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": "E"}
III = {"label": "III", "wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": "V"}
IV = {"label": "IV", "wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": "J"}
V = {"label": "V", "wiring": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": "Z"}
VI = {"label": "VI", "wiring": "JPGVOUMFYQBENHZRDKASXLICTW", "turnover": "ZM"}
VII = {"label": "VII", "wiring": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "turnover": "ZM"}
VIII = {"label": "VIII", "wiring": "FKQHTLXOCBJSPDZRAMEWNIUYGV", "turnover": "ZM",
}


# Reflectors
UKW_B = {"label": "UKW-B", "wiring": "YRUHQSLDPXNGOKMIEBFZCWVJAT"}
UKW_C = {"label": "UKW-C", "wiring": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}

# Special case, can be used with any Enigma
UKW_D = {
    "label": "UKW-D",
    "wiring": [
        "AB", "CD", "EF", "GH", "IK", "LM",
        "NO", "PQ", "RS", "TU", "VW", "XZ",
    ]
}

default_layout = [
    [16, 22, 4, 17, 19, 25, 20, 8, 14],
    [0, 18, 3, 5, 6, 7, 9, 10],
    [15, 24, 23, 2, 21, 1, 13, 12, 11],
]

# Enigma D and K
ENIGMA_D_K = {
    "stator": ETW_QWERTZ,
    "rotors": (
        {"label": "I", "wiring": "LPGSZMHAEOQKVXRFYBUTNICJDW", "turnover": "Y"},
        {"label": "II", "wiring": "SLVGBTFXJQOHEWIRZYAMKPCNDU", "turnover": "E"},
        {"label": "III", "wiring": "CJGDPSHKTURAWZXFMYNQOBVLIE", "turnover": "N"},
    ),
    "rotor_n": 3,
    "reflectors": (
        {"label": "UKW", "wiring": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        UKW_D,
    ),
    "rotatable_ref": True,
    "letter_group": 5,
    "plugboard": False,
    "numeric": False,
    "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "layout": default_layout
}


historical = {
    "Enigma I": {
        "stator": ETW,
        "rotors": (I, II, III, IV, V),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW-A", "wiring": "EJMZALYXVBWFCRQUONTSPIKHGD"},
            UKW_B,
            UKW_C,
            UKW_D,
        ),
        "rotatable_ref": False,
        "letter_group": 5,
        "plugboard": True,
        "numeric": True,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma M3": {
        "stator": ETW,
        "rotors": (I, II, III, IV, V, VI, VII, VIII),
        "rotor_n": 3,
        "reflectors": (UKW_B, UKW_C, UKW_D),
        "rotatable_ref": False,
        "letter_group": 5,
        "plugboard": True,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma M4": {
        "stator": ETW,
        "rotors": (
            I,
            II,
            III,
            IV,
            V,
            VI,
            VII,
            VIII,
            {"label": "Beta", "wiring": "LEYJVCNIXWPBQMDRTAKZGFUHOS"},
            {"label": "Gamma", "wiring": "FSOKANUERHMBTIYCWLQPZXVGJD"},
        ),
        "rotor_n": 4,
        "reflectors": (
            {"label": "UKW-b", "wiring": "ENKQAUYWJICOPBLMDXZVFTHRGS"},
            {"label": "UKW-c", "wiring": "RDOBJNTKVEHMLFCWZAXGYIPSUQ"},
            UKW_D,
        ),
        "rotatable_ref": False,
        "letter_group": 4,
        "plugboard": True,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Norenigma": {
        "stator": ETW,
        "rotors": (
            {
                "label": "I",
                "wiring": "WTOKASUYVRBXJHQCPZEFMDINLG",
                "turnover": "Q",
            },
            {
                "label": "II",
                "wiring": "GJLPUBSWEMCTQVHXAOFZDRKYNI",
                "turnover": "E",
            },
            {
                "label": "III",
                "wiring": "JWFMHNBPUSDYTIXVZGRQLAOEKC",
                "turnover": "V",
            },
            {
                "label": "IV",
                "wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
                "turnover": "J",
            },
            {
                "label": "V",
                "wiring": "HEJXQOTZBVFDASCILWPGYNMURK",
                "turnover": "Z",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "MOWJYPUXNDSRAIBFVLKZGQCHET"},
            UKW_D,
        ),
        "rotatable_ref": False,
        "letter_group": 5,
        "plugboard": True,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma G (A865)": {  # Zählwerk A865
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "LPGSZMHAEOQKVXRFYBUTNICJDW",
                "turnover": "SUVWZABCEFGIKLOPQ",
            },
            {
                "label": "II",
                "wiring": "SLVGBTFXJQOHEWIRZYAMKPCNDU",
                "turnover": "STVYZACDFGHKMNQ",
            },
            {
                "label": "III",
                "wiring": "CJGDPSHKTURAWZXFMYNQOBVLIE",
                "turnover": "UWXAEFHKMNR",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma G (G-111)": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "WLRHBQUNDKJCZSEXOTMAGYFPVI",
                "turnover": "SUVWZABCEFGIKLOPQ",
            },
            {
                "label": "II",
                "wiring": "TFJQAZWMHLCUIXRDYGOEVBNSKP",
                "turnover": "STVYZACDFGHKMNQ",
            },
            {
                "label": "III",
                "wiring": "QTPIXWVDFRMUSLJOHCANEZKYBG",
                "turnover": "SWZFHMQ",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma G (G-260)": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "RCSPBLKQAUMHWYTIFZVGOJNEXD",
                "turnover": "SUVWZABCEFGIKLOPQ",
            },
            {
                "label": "II",
                "wiring": "WCMIBVPJXAROSGNDLZKEYHUFQT",
                "turnover": "STVYZACDFGHKMNQ",
            },
            {
                "label": "III",
                "wiring": "FVDHZELSQMAXOKYIWPGCBUJTNR",
                "turnover": "UWXAEFHKMNR",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma G (G-312)": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "DMTWSILRUYQNKFEJCAZBPGXOHV",
                "turnover": "SUVWZABCEFGIKLOPQ",
            },
            {
                "label": "II",
                "wiring": "HQZGPJTMOBLNCIFDYAWVEUSRKX",
                "turnover": "STVYZACDFGHKMNQ",
            },
            {
                "label": "III",
                "wiring": "UQNTLSZFMREHDPXKIBVYGJCWOA",
                "turnover": "UWXAEFHKMNR",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "RULQMZJSYGOCETKWDAHNBXPVIF"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Enigma D": ENIGMA_D_K,
    "Enigma K": ENIGMA_D_K,
    "Enigma KD": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {"label": "I", "wiring": "VEZIOJCXKYDUNTWAPLQGBHSFMR", "turnover": "SUYAEHLNQ"},
            {
                "label": "II",
                "wiring": "HGRBSJZETDLVPMQYCXAOKINFUW",
                "turnover": "SUYAEHLNQ",
            },
            {
                "label": "III",
                "wiring": "NWLHXGRBYOJSAZDVTPKFQMEUIC",
                "turnover": "SUYAEHLNQ",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "KOTVPNLMJIAGHFBEWYXCZDQSRU"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Swiss K": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "PEZUOHXSCVFMTBGLRINQJWAYDK",
                "turnover": "Y",
            },
            {
                "label": "II",
                "wiring": "ZOUESYDKFWPCIQXHMVBLGNJRAT",
                "turnover": "E",
            },
            {
                "label": "III",
                "wiring": "EHRVXGAOBQUSIMZFLYNWKTPDJC",
                "turnover": "N",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "IMETCGFRAYSQBZXWLHKDVUPOJN"},
            UKW_D,
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout
    },
    "Railway": {
        "stator": ETW_QWERTZ,
        "rotors": (
            {
                "label": "I",
                "wiring": "JGDQOXUSCAMIFRVTPNEWKBLZYH",
                "turnover": "N",
            },
            {
                "label": "II",
                "wiring": "NTZPSFBOKMWRCJDIVLAEYUXHGQ",
                "turnover": "E",
            },
            {
                "label": "III",
                "wiring": "JVIUBHTCDYAKEQZPOSGXNRMWFL",
                "turnover": "Y",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "QYHOGNECVPUZTFDJAXWMKISRBL"},
            UKW_D,
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout,
        "numeric": False
    },
    "Tirpitz": {
        "stator": {"wiring": "KZROUQHYAIGBLWVSTDXFPNMCJE"},
        "rotors": (
            {
                "label": "I",
                "wiring": "KPTYUELOCVGRFQDANJMBSWHZXI",
                "turnover": "WZEKQ",
            },
            {
                "label": "II",
                "wiring": "UPHZLWEQMTDJXCAKSOIGVBYFNR",
                "turnover": "WZFLR",
            },
            {
                "label": "III",
                "wiring": "QUDLYRFEKONVZAXWHMGPJBSICT",
                "turnover": "WZEKQ",
            },
            {
                "label": "IV",
                "wiring": "CIWTBKXNRESPFLYDAGVHQUOJZM",
                "turnover": "WZFLR",
            },
            {
                "label": "V",
                "wiring": "UAXGISNJBVERDYLFZWTPCKOHMQ",
                "turnover": "YCFKR",
            },
            {
                "label": "VI",
                "wiring": "XFUZGALVHCNYSEWQTDMRBKPIOJ",
                "turnover": "XEIMQ",
            },
            {
                "label": "VII",
                "wiring": "BJVFTXPLNAYOZIKWGDQERUCHSM",
                "turnover": "YCFKR",
            },
            {
                "label": "VIII",
                "wiring": "YMTPNZHWKODAJXELUQVGCBISFR",
                "turnover": "XEIMQ",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "GEKPBTAUMOCNILJDXZYFHWVQSR"},
            UKW_D,
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "layout": default_layout,
        "numeric": False
    },
    "Enigma Z": {
        "stator": {"wiring": "0123456789"},
        "rotors": (
            {
                "label": "I",
                "wiring": "6418270359",
                "turnover": "9",
            },
            {
                "label": "II",
                "wiring": "5841097632",
                "turnover": "9",
            },
            {
                "label": "III",
                "wiring": "3581620794",
                "turnover": "9",
            },
        ),
        "rotor_n": 3,
        "reflectors": (
            {"label": "UKW", "wiring": "5079183642"},
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
        "charset": "1234567890",
        "layout": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], []]
    },
}


def format_position(charset, position, numeric=False):
    return "%02d" % (position) if numeric else charset[position-1]


class Plugboard:
    def __init__(self, pairs=None):
        self._pairs = []
        self.pairs(pairs)

    def pairs(self, pairs=None):
        """
        Sets plugboard pairs to the supplied pairs
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as
                                          strings or sublists with 2 chars)
                                          where each letter can only be used
                                          once
        :return: {dict} dictionary with pairs usable by the plugboard
        """
        if pairs is not None:
            self._pairs = pairs
        else:
            return self._pairs

    def route(self, letter):
        """
        Routes letter trough the wiring pair (if the letter is wired), otherwise
        returns the same letter
        :param letter: {char} input letter
        :return: {char} output routed letter
        """
        for pair in self._pairs:
            if letter in pair:
                return pair[0] if pair[0] != letter else pair[1]
        return letter


class _Component:  # Base component
    def __init__(self, label, wiring, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        self._label = label
        self._charset = charset
        self._max_index = len(charset)

        if len(wiring) != self._max_index:
            raise ValueError("Wiring must be the same length as the charset!")

        self._wiring = wiring

    def _forward(self, letter):
        return self._wiring[self._charset.index(letter)]

    def _backward(self, letter):
        return self._charset[self._wiring.index(letter)]

    def label(self):
        return self._label


class Stator(_Component):
    def __init__(self, wiring, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """
        :param wiring: {str} defines the way letters are routed
                             trough the rotor
        """
        super().__init__("ETW", wiring, charset=charset)

    def forward(self, letter):
        return super()._forward(letter)

    def backward(self, letter):
        return super()._backward(letter)


class _Rotatable(_Component):
    def __init__(self, label, wiring, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        super().__init__(label, wiring, charset=charset)

        self._offset = 0

    def offset(self, offset=None):
        """
        Sets offset of the rotor
        :param offset: {int} new rotor offset
        """
        if type(offset) is int:
            if offset not in range(1, 27):
                raise ValueError("Positions can only be set to values 1 - 26!")
            self._offset = offset - 1
        else:
            return self._offset + 1

    def position(self, numeric=False):
        """
        Returns current position (adjusted for ringstellung)
        :param numeric: {bool} whether or not the position should be numeric (02) for a letter (B)
        :return:
        """
        return format_position(self._charset, self._offset + 1, numeric)

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset. There are 26 letters in the
        alphabet so 26 is the max index!
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        self._offset = (self._offset + offset_by) % self._max_index


class Reflector(_Rotatable):
    def __init__(self, label, wiring, rotatable=False, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        super().__init__(label, wiring, charset)

        self.__rotatable = rotatable

    def rotatable(self):
        return self.__rotatable

    def reflect(self, letter):
        """
        Reflects letter sending it backwards into the 3 rotors
        :param letter: {char}
        :return: {char}
        """
        rel_input = (self._charset.index(letter) + self._offset) % self._max_index  # INT
        rel_result = self._charset.index(self._wiring[rel_input])  # INT
        abs_result = (rel_result - self._offset) % self._max_index
        return self._charset[abs_result]

    def offset(self, offset=None):
        if not self.__rotatable:
            raise ValueError("Non-rotatable reflectors don't have offset!")

        super().offset(offset)

    def rotate(self, by=1):
        if not self.__rotatable:
            raise ValueError("Non-rotatable reflectors can't be rotated!")

        super().rotate(by)

    def position(self, numeric=False):
        if not self.__rotatable:
            raise ValueError("Non-rotatable reflectors don't have a position!")

        return super().position(numeric)


class UKWD(Reflector):
    """UKW-D is a field-rewirable Enigma machine reflector"""

    def __init__(self, pairs):
        """
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as strings or sublists with 2 chars)
                      where each letter can only be used once
        """
        super().__init__("UKW-D", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", False, "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        self._marking = " ZXWVUTSRQPON MLKIHGFEDCBA"  # German notation
        self.wiring(pairs)

    def wiring(self, pairs=None):
        if pairs:
            if len(pairs) != 12:
                raise ValueError(
                    "There must be exactly 12 pairs for correct wiring!"
                )

            wiring = ["N"] + [""] * 12 + ["A"] + [""] * 12

            for pair in pairs:
                if "J" in pair or "Y" in pair:
                    raise ValueError("J and Y are hardwired!")

                a_index, b_index = map(self._marking.index, pair)

                wiring[a_index], wiring[b_index] = self._charset[b_index], self._charset[a_index]

            self._wiring = "".join(wiring)
        else:
            pairs = []
            for i, letter in enumerate(self._wiring):
                if letter == "A" or letter == "N":
                    continue

                pair = self._marking[i] + self._marking[self._charset.index(letter)]
                if not contains(pairs, pair):
                    pairs.append(pair)

            return pairs


class Rotor(_Rotatable):
    def __init__(self, label, wiring, turnover=None, charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        super().__init__(label, wiring, charset)

        self._turnover = turnover
        self._ring_offset = 0
        self._turnover = turnover

    def _adjusted_offset(self):
        return (self._offset - self._ring_offset) % self._max_index

    def forward(self, letter):
        """
        Routes the letter from the front board to the back board
        :param letter: {char}
        :return: {char}
        """
        rel_input = (
            self._charset.index(letter) + self._adjusted_offset()
        ) % self._max_index  # INT
        rel_result = self._charset.index(self._wiring[rel_input])  # INT
        return self._charset[(rel_result - self._adjusted_offset()) % self._max_index]

    def backward(self, letter):
        """
        Routes the letter from the back board to the front board
        :param letter: {char}
        :return: {char}
        """
        rel_input = (
            self._charset.index(letter) + self._adjusted_offset()
        ) % self._max_index  # INT
        rel_result = (
            self._wiring.index(self._charset[rel_input]) - self._adjusted_offset()
        ) % self._max_index  # INT
        return self._charset[rel_result]

    def ring_offset(self, offset=None):
        """
        Sets "Rinstellung" (ring settings) which can be misaligned with internal wiring
        :param setting: {int} new ring setting
        """
        if type(offset) == int:
            if offset not in range(1, 27):
                raise ValueError("Positions can only be set to values 1 - 26!")
            self._ring_offset = offset - 1
        else:
            return self._ring_offset + 1

    def in_turnover(self):
        """
        Returns True if the rotor is in turnover position else False
        :return: {bool} True if the rotor is in turnover position else False
        """
        return self.position() in self._turnover


class Enigma:
    """Universal Enigma object that supports every model except Enigma M4"""

    def __init__(
        self,
        model,
        reflector,
        rotors,
        stator,
        plugboard=True,
        plug_pairs=None,
        rotor_n=3,
        rotatable_ref=False,
        numeric=False,
        charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ):
        """
        :param reflector: {Reflector} Reflector object
        :param rotors: {[Rotor, Rotor, Rotor]} 3 or 4 rotors based on
                                               Enigma model
        :param stator: {Stator} Stator object
        """
        self._model = model
        self._rotor_n = rotor_n
        self._charset = charset

        # COMPONENTS
        self._reflector = reflector
        self._rotors = []
        self.rotors(rotors)
        self._stator = stator
        self._rotatable_ref = rotatable_ref

        # PLUGBOARD AND UHR
        self._plugboard = Plugboard(plug_pairs) if plugboard else None
        if self._plugboard is None:
            self._plugboard_route = lambda letter, _=None: letter
        else:
            self._plugboard_route = lambda letter, _=None: self._plugboard.route(letter)
        self._storage = Uhr()  # Stores currently unused object
        self._numeric = numeric

    def rotor_n(self):
        if self._reflector.label() == "UKW-D":
            return 3
        return self._rotor_n

    def press_key(self, key):
        """
        Simulates effects of pressing an Enigma keys (returning the routed
        result)
        :param key: {char} letter to encrypt
        """
        if key not in self.charset():
            raise ValueError("This Enigma instance does not have a '%s' key!" % key)

        if self._rotors[-1].in_turnover():
            self._rotors[-2].rotate()
        if self._rotors[-2].in_turnover():
            self._rotors[-2].rotate()
            self._rotors[-3].rotate()
        self._rotors[-1].rotate()

        output = self._plugboard_route(key)
        output = self._stator.forward(output)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self._reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        output = self._stator.backward(output)

        output = self._plugboard_route(output, True)

        return output

    # REFLECTOR

    def model(self):
        return self._model

    def reflector(self, new_reflector=None):
        if new_reflector:
            self._reflector = new_reflector
        else:
            return self._reflector.label()

    def reflector_pairs(self, new_pairs=None):
        if self._reflector.label() != "UKW-D":
            raise ValueError("Only UKW-D reflector has wiring pairs!")

        return self._reflector.wiring(new_pairs)

    def reflector_rotatable(self):
        return self._rotatable_ref

    def rotate_reflector(self, by=1):
        self._reflector.rotate(by)

    def reflector_position(self, new_position=None):
        if type(new_position) == int:
            if type(new_position) == str:
                new_position = self._charset.index(new_position)
            self._reflector.offset(new_position)
        else:
            return self._reflector.position()

    # ROTOR

    def rotate_rotor(self, index, by=1):
        self._rotors[index].rotate(by)

    def positions(self, new_positions=None):
        """
        Sets positions of all rotors
        Accepted types of indexes are
        a) Letters: "A", "B", ..., "Z"
        b) Numbers: 1, 1, ..., 26
        c) Numbers of type string: "01", "02", ..., "26"

        :param new_positions: {iterable}
        """
        if new_positions:
            for position, rotor in zip(new_positions, self._rotors):
                if type(position) == str:
                    if position in self._charset:
                        position = self._charset.index(position) + 1
                    else:
                        position = int(position)
                elif type(position) != int:
                    print("Invalid position type!")

                rotor.offset(position)
        else:
            return tuple(
                [rotor.position(self._numeric) for rotor in self._rotors]
            )

    def ring_settings(self, new_ring_settings=None):
        """
        Returns rotor positions, internal ring settings are different than the
        real ones! (01 in normal notation is 00 in internal notation)
        :param new_ring_settings: {[int, int, int]} new ring settings
        """
        if new_ring_settings:
            for setting, rotor in zip(new_ring_settings, self._rotors):
                rotor.ring_offset(setting)
        else:
            return [rotor.ring_offset() for rotor in self._rotors]

    def rotors(self, new_rotors=None):  # TODO: Add
        if new_rotors:
            if len(new_rotors) != self.rotor_n():
                raise ValueError("This enigma has %d rotors!" % self.rotor_n())

            self._rotors = new_rotors
        else:
            return [rotor.label() for rotor in self._rotors]

    # PLUGBOARD AND UHR

    def plug_pairs(self, new_plug_pairs=None):
        if self._plugboard is not None:
            return self._plugboard.pairs(new_plug_pairs)
        else:
            raise ValueError("This Enigma model doesn't have a plugboard!")

    def uhr(self, action=None):
        if not action:
            return isinstance(self._plugboard, Uhr)
        elif action == 'connect':
            if isinstance(self._storage, Uhr):
                self._storage, self._plugboard = self._plugboard, self._storage
                self._plugboard.pairs([])
                self._plugboard_route = self._plugboard.route
        elif action == 'disconnect' and isinstance(self._plugboard, Uhr):
            self._storage, self._plugboard = self._plugboard, self._storage
            self._plugboard.pairs([])
            self._plugboard_route = lambda letter, _=None: self._plugboard.route(letter)
        else:
            raise ValueError("Invalid action!")

    def uhr_position(self, new_position=None):
        if not isinstance(self._plugboard, Uhr):
            raise ValueError("Can't set uhr position - uhr not connected!")

        if type(new_position) == int:
            self._plugboard.position(new_position)
        else:
            return self._plugboard.position()

    def charset(self):
        """
        Returns charset of this Enigma machine
        """
        return self._charset
