#!/usr/bin/env python3

from string import ascii_uppercase as alphabet

from enigma.core.extensions import Uhr

# Stators
ETW = {"wiring": alphabet}
ETW_QWERTZ = {"wiring": "QWERTZUIOASDFGHJKPYXCVBNML"}

# Rotors
I = {"label": "I", "wiring": "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "turnover": "Q"}
II = {"label": "II", "wiring": "AJDKSIRUXBLHWTMCQGZNPYFVOE", "turnover": "E"}
III = {"label": "III", "wiring": "BDFHJLCPRTXVZNYEIWGAKMUSQO", "turnover": "V"}
IV = {"label": "IV", "wiring": "ESOVPZJAYQUIRHXLNFTGKDCMWB", "turnover": "J"}
V = {"label": "V", "wiring": "VZBRGITYUPSDNHLXAWMJQOFECK", "turnover": "Z"}
VI = {"label": "VI", "wiring": "JPGVOUMFYQBENHZRDKASXLICTW", "turnover": "ZM"}
VII = {"label": "VII", "wiring": "NZJHGRCXMYSWBOUFAIVLPEKQDT", "turnover": "ZM"}
VIII = {
    "label": "VIII",
    "wiring": "FKQHTLXOCBJSPDZRAMEWNIUYGV",
    "turnover": "ZM",
}


# Reflectors
UKW_B = {"label": "UKW-B", "wiring": "YRUHQSLDPXNGOKMIEBFZCWVJAT"}
UKW_C = {"label": "UKW-C", "wiring": "FVPJIAOYEDRZXWGCTKUQSBNMHL"}

# Special case, can be used with any Enigma
UKW_D = {
    "label": "UKW-D",
    "wiring": [
        "AB",
        "CD",
        "EF",
        "GH",
        "IK",
        "LM",
        "NO",
        "PQ",
        "RS",
        "TU",
        "VW",
        "XZ",
    ],
}


# Enigma D and K
ENIGMA_D_K = {
    "stator": ETW_QWERTZ,
    "rotors": (
        {"label": "I", "wiring": "LPGSZMHAEOQKVXRFYBUTNICJDW", "turnover": "Y"},
        {
            "label": "II",
            "wiring": "SLVGBTFXJQOHEWIRZYAMKPCNDU",
            "turnover": "E",
        },
        {
            "label": "III",
            "wiring": "CJGDPSHKTURAWZXFMYNQOBVLIE",
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
}


historical_data = {
    "Enigma1": {
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
    },
    "EnigmaM3": {
        "stator": ETW,
        "rotors": (I, II, III, IV, V, VI, VII, VIII),
        "rotor_n": 3,
        "reflectors": (UKW_B, UKW_C, UKW_D),
        "rotatable_ref": False,
        "letter_group": 5,
        "plugboard": True,
        "numeric": False,
    },
    "EnigmaM4": {
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
    },
    "EnigmaG": {
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
            UKW_D,
        ),
        "rotatable_ref": True,
        "letter_group": 5,
        "plugboard": False,
        "numeric": False,
    },
    "EnigmaD": ENIGMA_D_K,
    "EnigmaK": ENIGMA_D_K,
    "SwissK": {
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
        "numeric": False,
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
    },
}


def format_position(position, numeric=False):
    return "%02d" % (position + 1) if numeric else alphabet[position]


class Plugboard:
    def __init__(self, pairs=None):
        self._pairs = []
        self.pairs(pairs)

    def pairs(self, pairs=None):
        """
        Sets plugboard pairs to the supplied pairs
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as strings or sublists with 2 chars)
                      where each letter can only be used once
        :return: {dict} dictionary with pairs usable by the plugboard
        """
        if pairs is not None:
            self._pairs = pairs
        else:
            return self._pairs

    def route(self, letter):
        """
        Routes letter trough the wiring pair (if the letter is wired), otherwise returns the same letter
        :param letter: {char} input letter
        :return: {char} output routed letter
        """
        for pair in self._pairs:
            if letter in pair:
                return pair[0] if pair[0] != letter else pair[1]
        return letter


class _Component:  # Base component
    def __init__(self, label, wiring):
        self._label = label

        if len(wiring) != 26:
            raise ValueError("Wiring must be of same length as the alphabet!")

        self._wiring = wiring

    def _forward(self, letter):
        return self._wiring[alphabet.index(letter)]

    def _backward(self, letter):
        return alphabet[self._wiring.index(letter)]

    def label(self):
        return self._label


class Stator(_Component):
    def __init__(self, wiring):
        """
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        super().__init__("ETW", wiring)

    def forward(self, letter):
        return super()._forward(letter)

    def backward(self, letter):
        return super()._backward(letter)


class _Rotatable(_Component):
    def __init__(self, label, wiring):
        super().__init__(label, wiring)

        self._offset = 0

    def offset(self, offset=None):
        """
        Sets offset of the rotor
        :param offset: {int} new rotor offset
        """
        if offset is not None:
            self._offset = offset % 26
        else:
            return self._offset

    def position(self, numeric=False):
        """
        Returns current position (adjusted for ringstellung)
        :param numeric: {bool} whether or not the position should be numeric (02) for a letter (B)
        :return:
        """
        return format_position(self._offset, numeric)

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset. There are 26 letters in the
        alphabet so 26 is the max index!
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        self.offset(self._offset + offset_by)


class Reflector(_Rotatable):
    def __init__(self, label, wiring, rotatable=False):
        super().__init__(label, wiring)

        self.__rotatable = rotatable

    def rotatable(self):
        return self.__rotatable

    def reflect(self, letter):
        """
        Reflects letter sending it backwards into the 3 rotors
        :param letter: {char}
        :return: {char}
        """
        rel_input = (alphabet.index(letter) + self._offset) % 26  # INT
        rel_result = alphabet.index(self._wiring[rel_input])  # INT
        abs_result = (rel_result - self._offset) % 26
        return alphabet[abs_result]

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
        super().__init__("UKW-D", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", False)

        self._marking = " ZXWVUTSRQPON MLKIHGFEDCBA"  # German notation
        self.wiring(pairs)

    def wiring(self, pairs=None):
        if pairs is not None:
            if len(pairs) != 12:
                raise ValueError(
                    "There must be exactly 12 pairs for correct wiring!"
                )

            wiring = ["N"] + [""] * 12 + ["A"] + [""] * 12

            for pair in pairs:
                if "J" in pair or "Y" in pair:
                    raise ValueError("J and Y are hardwired!")

                a, b = pair
                a_index = self._marking.index(a)
                b_index = self._marking.index(b)

                wiring[a_index] = alphabet[b_index]
                wiring[b_index] = alphabet[a_index]

            self._wiring = "".join(wiring)
        else:
            pairs = []
            for i, letter in enumerate(self._wiring):
                if letter == "A" or letter == "N":
                    continue

                pair = self._marking[i] + self._marking[alphabet.index(letter)]
                if pair[::-1] not in pairs:
                    pairs.append(pair)

            return pairs


class Rotor(_Rotatable):
    def __init__(self, label, wiring, turnover=None):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        super().__init__(label, wiring)

        self._turnover = turnover
        self._ring_offset = 0
        self._turnover = turnover

    def _adjusted_offset(self):
        return (self._offset - self._ring_offset) % 26

    def forward(self, letter):
        """
        Routes the letter from the front board to the back board
        :param letter: {char}
        :return: {char}
        """
        rel_input = (
            alphabet.index(letter) + self._adjusted_offset()
        ) % 26  # INT
        rel_result = alphabet.index(self._wiring[rel_input])  # INT
        return alphabet[(rel_result - self._adjusted_offset()) % 26]

    def backward(self, letter):
        """
        Routes the letter from the back board to the front board
        :param letter: {char}
        :return: {char}
        """
        rel_input = (
            alphabet.index(letter) + self._adjusted_offset()
        ) % 26  # INT
        rel_result = (
            self._wiring.index(alphabet[rel_input]) - self._adjusted_offset()
        ) % 26  # INT
        return alphabet[rel_result]

    def ring_offset(self, offset=None):
        """
        Sets "Rinstellung" (ring settings) which can be misaligned with internal wiring
        :param setting: {int} new ring setting
        """
        if offset is not None:
            self._ring_offset = offset % 26
        return self._ring_offset

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
    ):
        """
        :param reflector: {Reflector} Reflector object
        :param rotors: {[Rotor, Rotor, Rotor]} 3 or 4 rotors based on
                                               Enigma model
        :param stator: {Stator} Stator object
        """
        self._model = model
        self._rotor_n = rotor_n

        # COMPONENTS
        self._reflector = reflector
        self._rotors = []
        self.rotors(rotors)
        self._stator = stator
        self._rotatable_ref = rotatable_ref

        # PLUGBOARD AND UHR
        self._plugboard = Plugboard(plug_pairs) if plugboard else None
        self._uhr = None
        self._numeric = numeric

    def rotor_n(self):
        if self._reflector.label() == "UKW-D":
            return 3
        else:
            return self._rotor_n

    def _route(self, letter, backwards=False):
        if self._uhr is not None:
            return self._uhr.route(letter, backwards)
        elif self._plugboard is not None:
            return self._plugboard.route(letter)
        return letter

    def press_key(self, key):
        """
        Simulates effects of pressing an Enigma keys (returning the routed
        result)
        :param key: {char} letter to encrypt
        """
        self.step_rotors()

        output = self._route(key)

        output = self._stator.forward(output)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self._reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        output = self._stator.backward(output)

        output = self._route(output, True)

        return output

    def step_rotors(self):
        """Advance rotor positions, the fourth rotor is not included because
        it never rotates"""
        if self._rotors[-1].in_turnover():
            self._rotors[-2].rotate()

        if self._rotors[-2].in_turnover():
            self._rotors[-2].rotate()
            self._rotors[-3].rotate()

        self._rotors[-1].rotate()

    # REFLECTOR

    def model(self):
        return self._model

    def reflector(self, new_reflector=None):
        if new_reflector is not None:
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
        if new_position is not None:
            if type(new_position) == str:
                new_position = alphabet.index(new_position)
            self._reflector.offset(new_position)
        else:
            return self._reflector.position()

    # ROTOR

    def rotate_rotor(self, index, by=1):
        self._rotors[index].rotate(by)

    def positions(self, new_positions=None):
        """
        Sets positions of all rotors
        :param new_positions: {[int, int, int]} or {[char, char, char]} new
                              positions to be set on the Enigma
        """
        if new_positions is not None:
            if not (
                all([type(pos) == str for pos in new_positions])
                or all([type(pos) == int for pos in new_positions])
            ):
                raise ValueError("Mixed numeric and string positions!")

            for position, rotor in zip(new_positions, self._rotors):
                if type(position) == str:
                    if position in alphabet:
                        position = alphabet.index(position)
                    else:
                        position = int(position) - 1
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
        if new_ring_settings is not None:
            for setting, rotor in zip(new_ring_settings, self._rotors):
                rotor.ring_offset(setting - 1)
        else:
            return [rotor.ring_offset() + 1 for rotor in self._rotors]

    def rotors(self, new_rotors=None):
        if new_rotors is not None:
            if len(new_rotors) != self.rotor_n():
                raise ValueError("This enigma has %d rotors!" % self.rotor_n())

            self._rotors = new_rotors
        else:
            return [rotor.label() for rotor in self._rotors]

    # PLUGBOARD AND UHR

    def plug_pairs(self, new_plug_pairs=None):
        if self._uhr is not None:
            return self._uhr.pairs(new_plug_pairs)
        else:
            if self._plugboard is not None:
                return self._plugboard.pairs(new_plug_pairs)
            else:
                return ""

    def uhr(self, connect=None):
        if connect is None:
            return self._uhr is not None
        else:
            if connect:
                self._uhr = Uhr()
            else:
                del self._uhr
                self._uhr = None

    def uhr_position(self, new_position=None):
        if self._uhr is None:
            raise ValueError("Can't set uhr position - uhr not connected!")

        if new_position is not None:
            self._uhr.position(new_position)
        else:
            return self._uhr.position()
