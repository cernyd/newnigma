#!/usr/bin/env python3
# *-* coding: utf-8 *-*


from string import ascii_uppercase as alphabet


zur_beachtung = """\
Zur Beachtung!
Beachte die Gebrauchsanleitung für die Chiffriermaschine (H. Dv. g. 13)

1. Zur Säuberung der Walzenkontakte alle Walzen mehrmals gegenseitig vor- und rückwärtsdrehen.

2. Zur Säuberung der Tastenkontakte sämtliche Tasten vor Einschaltung des Stromes mehrmals kräftig herunterdrücken und
hochschnellen lassen, wobei eine Taste dauernd gedrückt bleibt.

3. Bei Einstellung der in den Fenstern sichtbaren Zeichen beachten, daß die Walzen richtig gerastet sind.

4. Die unverwechselbaren doppelpoligen Stecker sind bis zum Anschlag in ihre Buchsenpaare einzuführen.
Die vordere Holzklappe ist danach zu schließen, da sonst 3 Lampen zugleich aufleuchten können.

5. Leuchtet bei Tastendruck keine Lampe auf, so sind die Batterie, ihre Kontaktfedern, ihre Anschlüsse am
Umschalter und der Umschalter zu prüfen.

6. Leuchten bei Tastendruck eine oder mehrere Lampen nicht auf, so sind die entsprechenden Lampen, die
Kontakte unter ihnen, die Kabel der doppelpoligen Stecker, die Steckerbuchsen einschließlich ihrer Kurzschlußbleche,
die Walzenkontakte, die Arbeitskontakte unter den jeweils gedrückten Tasten und die Ruhekontakte unter den mit ihnen
korrespondierenden Tasten zu prüfen und bei etwa vorhandenen Verschmutzungen und Oxydationen zu säubern. (Siehe auch Ziffer 2).
Von Maschine Nr. A 4388 ab dient zur Lampenprüfung die Öffnung auf der rechten Lampenfeldseite.
Von Maschine Nr. A 4388 ab dienen zur Kabelprüfung die äußerste linke und rechte Buchse der mittleren
Reihe am Steckerbrett und die Kabelprüflampe auf der linken Lampenfeldseite.

7. Walzenachse und Walzenbuchsen sind sauber zu halten und wie alle übrigen Lagerstellen hin und
wieder mit harz- und säurefreiem Öl leicht einzufetten. Die festen Kontakte der Walzen sind alle
6–8 Wochen mit Polierpapier überzuschleifen und mit einem wenig getränkten Öllappen abzureiben.
Die Tastenkontakte, die Lampenkontakte und die Kurzschlußbleche sind vor Öl zu schützen.

8. Schlüsselangaben erfolgen entweder durch Zahlen oder Buchstaben.
Zum Umsetzen der Zahlen in Buchstaben oder umgekehrt dient nachstehende Tafel:

A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
"""


labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12', 'M-13',
          'N-14', 'O-15', 'P-16', 'Q-17', 'R-18', 'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26']

# For the GUI plug board
layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14], [0, 18, 3, 5, 6, 7, 9, 10], [15, 24, 23, 2, 21, 1, 13, 12, 11]]


# Stators
ETW = {'wiring': alphabet}
ETW_QWERTZ = {'wiring': "QWERTZUIOASDFGHJKPYXCVBNML"}

# Rotors
I = {'label': 'I', 'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'turnover': 'Q'}
II = {'label': 'II', 'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'turnover': 'E'}
III = {'label': 'III', 'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'turnover': 'V'}
IV = {'label': 'IV', 'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'turnover': 'J'}
V = {'label': 'V', 'wiring': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'turnover': 'Z'}
VI = {'label': 'VI', 'wiring': 'JPGVOUMFYQBENHZRDKASXLICTW', 'turnover': 'ZM'}
VII = {'label': 'VII', 'wiring': 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'turnover': 'ZM'}
VIII = {'label': 'VIII', 'wiring': 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'turnover': 'ZM'}


# Reflectors
UKW_B = {'label': 'UKW-B', 'wiring': "YRUHQSLDPXNGOKMIEBFZCWVJAT"}
UKW_C = {'label': 'UKW-C', 'wiring': "FVPJIAOYEDRZXWGCTKUQSBNMHL"}


# Enigma D and K
ENIGMA_D_K = {
    'stator' : ETW_QWERTZ,
    'rotors': (
        {'label': 'I', 'wiring': 'LPGSZMHAEOQKVXRFYBUTNICJDW', 'turnover': 'Y'},
        {'label': 'II', 'wiring': 'SLVGBTFXJQOHEWIRZYAMKPCNDU', 'turnover': 'E'},
        {'label': 'III', 'wiring': 'CJGDPSHKTURAWZXFMYNQOBVLIE', 'turnover': 'N'},
    ),
    'reflectors': (
        {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
    )
}


historical_data = {
    'Enigma1': {
        'stator': ETW,
        'rotors': (I, II, III, IV, V),
        'reflectors': (
            {'label': 'UKW-A', 'wiring': "EJMZALYXVBWFCRQUONTSPIKHGD"}, UKW_B, UKW_C
        )
    },
    'EnigmaM3': {
        'stator': ETW,
        'rotors': (I, II, III, IV, V, VI, VII, VIII),
        'reflectors': (UKW_B, UKW_C)
    },
    'EnigmaM4': {
        'stator': ETW,
        'rotors': (
            I, II, III, IV, V, VI, VII, VIII,
            {'label': 'Beta', 'wiring': 'LEYJVCNIXWPBQMDRTAKZGFUHOS'},
            {'label': 'Gamma', 'wiring': 'FSOKANUERHMBTIYCWLQPZXVGJD'}
        ),
        'reflectors': (
            {'label': 'UKW-b', 'wiring': "ENKQAUYWJICOPBLMDXZVFTHRGS"},
            {'label': 'UKW-c', 'wiring': "RDOBJNTKVEHMLFCWZAXGYIPSUQ"}
        )
    },
    'Norenigma': {
        'stator': ETW,
        'rotors': (
            {'label': 'I', 'wiring': 'WTOKASUYVRBXJHQCPZEFMDINLG', 'turnover': 'Q'},
            {'label': 'II', 'wiring': 'GJLPUBSWEMCTQVHXAOFZDRKYNI', 'turnover': 'E'},
            {'label': 'III', 'wiring': 'JWFMHNBPUSDYTIXVZGRQLAOEKC', 'turnover': 'V'},
            {'label': 'IV', 'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'turnover': 'J'},
            {'label': 'V', 'wiring': 'HEJXQOTZBVFDASCILWPGYNMURK', 'turnover': 'Z'}
        ),
        'reflectors': (
            {'label': 'UKW', 'wiring': "MOWJYPUXNDSRAIBFVLKZGQCHET"},
        )
    },
    'EnigmaG': {
        'stator': ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'wiring': 'LPGSZMHAEOQKVXRFYBUTNICJDW', 'turnover': 'SUVWZABCEFGIKLOPQ'},
            {'label': 'II', 'wiring': 'SLVGBTFXJQOHEWIRZYAMKPCNDU', 'turnover': 'STVYZACDFGHKMNQ'},
            {'label': 'III', 'wiring': 'CJGDPSHKTURAWZXFMYNQOBVLIE', 'turnover': 'UWXAEFHKMNR'},
        ),
        'reflectors': (
            {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        )
    },
    'EnigmaD': ENIGMA_D_K,
    'EnigmaK': ENIGMA_D_K,
    'SwissK': {
        'stator' : ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'wiring': 'PEZUOHXSCVFMTBGLRINQJWAYDK', 'turnover': 'Y'},
            {'label': 'II', 'wiring': 'ZOUESYDKFWPCIQXHMVBLGNJRAT', 'turnover': 'E'},
            {'label': 'III', 'wiring': 'EHRVXGAOBQUSIMZFLYNWKTPDJC', 'turnover': 'N'},
        ),
        'reflectors': (
            {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        )
    },
    'Railway': {
        'stator': ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'wiring': 'JGDQOXUSCAMIFRVTPNEWKBLZYH', 'turnover': 'N'},
            {'label': 'II', 'wiring': 'NTZPSFBOKMWRCJDIVLAEYUXHGQ', 'turnover': 'E'},
            {'label': 'III', 'wiring': 'JVIUBHTCDYAKEQZPOSGXNRMWFL', 'turnover': 'Y'},
        ),
        'reflectors': (
            {'label': 'UKW', 'wiring': "QYHOGNECVPUZTFDJAXWMKISRBL"},
        )
    },
    'Tirpitz': {
        'stator': {'label': 'ETW', 'back_board': "KZROUQHYAIGBLWVSTDXFPNMCJE"},
        'rotors': (
            {'label': 'I', 'wiring': 'KPTYUELOCVGRFQDANJMBSWHZXI', 'turnover': 'WZEKQ'},
            {'label': 'II', 'wiring': 'UPHZLWEQMTDJXCAKSOIGVBYFNR', 'turnover': 'WZFLR'},
            {'label': 'III', 'wiring': 'QUDLYRFEKONVZAXWHMGPJBSICT', 'turnover': 'WZEKQ'},
            {'label': 'IV', 'wiring': 'CIWTBKXNRESPFLYDAGVHQUOJZM', 'turnover': 'WZFLR'},
            {'label': 'V', 'wiring': 'UAXGISNJBVERDYLFZWTPCKOHMQ', 'turnover': 'YCFKR'},
            {'label': 'VI', 'wiring': 'XFUZGALVHCNYSEWQTDMRBKPIOJ', 'turnover': 'XEIMQ'},
            {'label': 'VII', 'wiring': 'BJVFTXPLNAYOZIKWGDQERUCHSM', 'turnover': 'YCFKR'},
            {'label': 'VIII', 'wiring': 'YMTPNZHWKODAJXELUQVGCBISFR', 'turnover': 'XEIMQ'}
        ),
        'reflectors': (
            {'label': 'UKW', 'wiring': "GEKPBTAUMOCNILJDXZYFHWVQSR"},
        )
    }
}


def init_component(model, comp_type, label=None):
    """
    Initializes a Stator, Rotor or Reflector.
    :param model: {str} Enigma machine model
    :param comp_type: {str} "Stator", "Rotor" or "Reflector"
    :param label: {str} or {int} Component label like "I", "II", "UKW-B" or numerical index
                  of their position in historical data (0 = "I", 2 = "II", ...)
    """
    data = historical_data[model]

    if label is None and comp_type != "Stator":
        raise TypeError("A label has to be supplied for Rotor and Reflector" \
                        "object!")

    assert model in historical_data, "The model argument must be in historical" \
                                     "Enigma models!"

    i = 0
    if comp_type == "Rotor":
        for rotor in data["rotors"]:
            if rotor['label'] == label or label == i:
                return Rotor(**rotor)
            i += 1
    elif comp_type == "Reflector":
        for reflector in data["reflectors"]:
            if reflector['label'] == label or label == i:
                return Reflector(**reflector)
            i += 1
    elif comp_type == "Stator":
        return Stator(**data["stator"])
    else:
        raise TypeError('The comp_type must be "Reflector", "Stator" or "Rotor"')


def init_enigma(model, rotor_labels, reflector_label):
    rotors = []
    for label in rotor_labels:
        rotors.append(init_component(model, "Rotor", label))

    reflector = init_component(model, "Reflector", reflector_label)
    stator = init_component(model, "Stator")

    return Enigma(model, reflector, rotors, stator)


class Plugboard:
    def __init__(self, pairs=None):
        self.pairs = {}
        self.set_plug_pairs(pairs)

    def set_plug_pairs(self, pairs=None):
        """
        Sets plugboard pairs to the supplied pairs
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as strings or sublists with 2 chars)
                      where each letter can only be used once
        :return: {dict} dictionary with pairs usable by the plugboard
        """
        result_pairs = {}

        if pairs is None:
            return {}

        for pair in pairs:
            a, b = pair
            result_pairs[a] = b
            result_pairs[b] = a

        self.pairs = result_pairs

    def route(self, letter):
        """
        Routes letter trough the wiring pair (if the letter is wired), otherwise returns the same letter
        :param letter: {char} input letter
        :return: {char} output routed letter
e       """
        return self.pairs.get(letter, letter)


class Stator:
    def __init__(self, wiring):
        """
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        # Pairs of letters FRONT <-> BACK
        self.wiring = wiring

    def forward(self, letter):
        return self.wiring[alphabet.index(letter)]

    def backward(self, letter):
        return alphabet[self.wiring.index(letter)]


class Reflector:
    def __init__(self, label, wiring):
        self.wiring = wiring
        self.label = label

    def reflect(self, letter):
        """
        Reflects letter sending it backwards into the 3 rotors
        :param letter: {char}
        :return: {char}
        """
        return self.wiring[alphabet.index(letter)]


class UKWD(Plugboard):
    """UKW - D is a field-rewirable Enigma machine reflector"""

    def __init__(self, pairs):
        """
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as strings or sublists with 2 chars)
                      where each letter can only be used once
        """
        super().__init__(pairs)
        self.plugboard = Plugboard(pairs)

    def reflect(self, letter):  # TODO: This might not be the best inheritance strategy
        """
        Reflects letter sending it backwards into the 3 rotors
        :param letter: {char}
        :return: {char}
        """
        return self.route(letter)


class Uhr:
    pass


class Rotor:
    def __init__(self, label, wiring, turnover=None):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        self.wiring = [alphabet.index(letter) for letter in wiring]

        self.label = label
        self.offset = 0  # "Stellung"
        self.ring_offset = 0  # "Ringstellung"
        self.turnover = turnover

    def forward(self, letter):
        """
        Routes the letter from the front board to the back board
        :param letter: {char}
        :return: {char}
        """
        relative_input = self.apply_offset(alphabet.index(letter))
        relative_result = self.wiring[relative_input]
        return alphabet[self.apply_offset(relative_result, True)]

    def backward(self, letter):
        """
        Routes the letter from the back board to the front board
        :param letter: {char}
        :return: {char}
        """
        relative_input = self.apply_offset(alphabet.index(letter))
        relative_result = self.apply_offset(self.wiring.index(relative_input), True)
        return alphabet[relative_result]

    def apply_offset(self, i, negate=False):
        """
        Applies either positive or negative offset to a value
        :param i: {int} incoming position
        :param negate: {bool} subtract the offset rather than add
        :return: {int} the offset value
        """
        offset = (self.offset - self.ring_offset) % 26
        offset = -offset if negate else offset
        return (i + offset) % 26  # The alphabet has 27 - 1 letters (and index is counted from 0)

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset. There are 26 letters in the
        alphabet so 26 is the max index!
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        self.offset = (self.offset + offset_by) % 26

    def set_offset(self, offset):
        """
        Sets offset of the rotor
        :param offset: {int} new rotor offset
        """
        self.offset = offset % 26

    def set_ring(self, setting):
        """
        Sets "Rinstellung" (ring settings) which can be misaligned with internal wiring
        :param setting: {int} new ring setting
        """
        self.ring_offset = setting % 26

    def position(self, numeric=False):
        """
        Returns current rotor position (adjusted for ringstellung)
        :param numeric: {bool} whether or not the position should be numeric (02) for a letter (B)
        :return:
        """
        # Shown position does not need to equat the actual position because the labels can be
        # rotated using "Ringstellung"
        return "%02d" % (self.offset + 1) if numeric else alphabet[self.offset]

    @property
    def in_turnover(self):
        """
        Returns True if the rotor is in turnover position else False
        :return: {bool} True if the rotor is in turnover position else False
        """
        return self.position() in self.turnover


class Enigma:
    """Universal Enigma object that supports every model except Enigma M4"""
    def __init__(self, model, reflector, rotors, stator, plug_pairs=None):
        """
        :param reflector: {Reflector} Reflector object
        :param rotors: {[Rotor, Rotor, Rotor]} 3 or 4 rotors based on
                                               Enigma model
        :param stator: {Stator} Stator object
        """
        self.model = model
        self._reflector = reflector

        if model == "EnigmaM4":
            assert len(rotors) == 4, "Enigma M4 model must have " \
                                     "exactly 4 rotors!"
        elif model in historical_data:
            assert len(rotors) == 3, "%s model must have " \
                                    "exactly 3 rotors!" % model
        else:
            raise AssertionError('Invalid Enigma model "%s"' % model)

        self.rotors = rotors
        self._stator = stator
        self._plugboard = Plugboard(plug_pairs)

    def step_rotors(self):
        """Advance rotor positions"""
        if self.rotors[-1].in_turnover:
            self.rotors[-2].rotate()

        if self.rotors[-2].in_turnover:
            self.rotors[-2].rotate()
            self.rotors[-3].rotate()

        self.rotors[-1].rotate()

    @property
    def positions(self):
        """
        Returns rotor positions
        :return: {[int, int, int]}
        """
        return [rotor.position() for rotor in self.rotors]

    @positions.setter
    def positions(self, new_positions):
        """
        Sets positions of all rotors
        :param new_positions: {[int, int, int]} or {[char, char, char]} new positions to be set on the Enigma
        """
        assert all([type(pos) == str for pos in new_positions]) or all([type(pos) == int for pos in new_positions])

        for position, rotor in zip(new_positions, self.rotors):
            if type(position) == str:
                position = alphabet.index(position)
            rotor.set_offset(position)

    @property
    def ring_settings(self):
        """
        Returns rotor positions
        :return: {[int, int, int]}
        """
        return [rotor.ring_offset for rotor in self.rotors]

    @ring_settings.setter
    def ring_settings(self, new_ring_settings):
        """
        Returns rotor positions
        :param new_ring_settings: {[int, int, int]} new ring settings
        """
        for setting, rotor in zip(new_ring_settings, self.rotors):
            rotor.set_ring(setting)

    def press_key(self, key):
        """
        Simulates effects of pressing an Enigma keys (returning the routed
        result)
        :param key: {char} letter to encrypt
        """
        self.step_rotors()

        output = self._plugboard.route(key)
        output = self._stator.forward(output)

        for rotor in reversed(self.rotors):
            output = rotor.forward(output)
        
        output = self._reflector.reflect(output)

        for rotor in self.rotors:
            output = rotor.backward(output)

        output = self._stator.backward(output)
        output = self._plugboard.route(output)

        return output

    def set_plug_pairs(self, plug_pairs):
        self._plugboard.set_plug_pairs(plug_pairs)

    def __str__(self):
        header = "=== %s instance data ===" % self.model
        footer = "="*len(header)
        message = "\nRotors:              %s\nRotor positions:     %s\nRotor ring settings: %s \nReflector: %s\n"  # \nPlugboard pairs: %s
        rotors = ' '.join([rotor.label for rotor in self.rotors])
        return header + message % (rotors, ' '.join(self.positions), ' '.join(map(str, self.ring_settings)), self._reflector.label) + footer
