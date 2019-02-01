#!/usr/bin/env python3

from string import ascii_uppercase as alphabet
from enigma.core.extensions import Uhr#, UKWD


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
    'rotor_n': 3,
    'reflectors': (
        {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
    ),
    'rotatable_ref': True,
    'letter_group': 5,
    'plugboard': False
}


historical_data = {
    'Enigma1': {
        'stator': ETW,
        'rotors': (I, II, III, IV, V),
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW-A', 'wiring': "EJMZALYXVBWFCRQUONTSPIKHGD"}, UKW_B, UKW_C
        ),
        'rotatable_ref': False,
        'letter_group': 5,
        'plugboard': True
    },
    'EnigmaM3': {
        'stator': ETW,
        'rotors': (I, II, III, IV, V, VI, VII, VIII),
        'rotor_n': 3,
        'reflectors': (UKW_B, UKW_C),
        'rotatable_ref': False,
        'letter_group': 5,
        'plugboard': True
    },
    'EnigmaM4': {
        'stator': ETW,
        'rotors': (
            I, II, III, IV, V, VI, VII, VIII,
            {'label': 'Beta', 'wiring': 'LEYJVCNIXWPBQMDRTAKZGFUHOS'},
            {'label': 'Gamma', 'wiring': 'FSOKANUERHMBTIYCWLQPZXVGJD'}
        ),
        'rotor_n': 4,
        'reflectors': (
            {'label': 'UKW-b', 'wiring': "ENKQAUYWJICOPBLMDXZVFTHRGS"},
            {'label': 'UKW-c', 'wiring': "RDOBJNTKVEHMLFCWZAXGYIPSUQ"}
        ),
        'rotatable_ref': False,
        'letter_group': 4,
        'plugboard': True
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
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW', 'wiring': "MOWJYPUXNDSRAIBFVLKZGQCHET"},
        ),
        'rotatable_ref': False,
        'letter_group': 5,
        'plugboard': True
    },
    'EnigmaG': {
        'stator': ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'wiring': 'LPGSZMHAEOQKVXRFYBUTNICJDW', 'turnover': 'SUVWZABCEFGIKLOPQ'},
            {'label': 'II', 'wiring': 'SLVGBTFXJQOHEWIRZYAMKPCNDU', 'turnover': 'STVYZACDFGHKMNQ'},
            {'label': 'III', 'wiring': 'CJGDPSHKTURAWZXFMYNQOBVLIE', 'turnover': 'UWXAEFHKMNR'},
        ),
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        ),
        'rotatable_ref': True,
        'letter_group': 5,
        'plugboard': False
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
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW', 'wiring': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        ),
        'rotatable_ref': True,
        'letter_group': 5,
        'plugboard': False
    },
    'Railway': {
        'stator': ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'wiring': 'JGDQOXUSCAMIFRVTPNEWKBLZYH', 'turnover': 'N'},
            {'label': 'II', 'wiring': 'NTZPSFBOKMWRCJDIVLAEYUXHGQ', 'turnover': 'E'},
            {'label': 'III', 'wiring': 'JVIUBHTCDYAKEQZPOSGXNRMWFL', 'turnover': 'Y'},
        ),
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW', 'wiring': "QYHOGNECVPUZTFDJAXWMKISRBL"},
        ),
        'rotatable_ref': True,
        'letter_group': 5,
        'plugboard': False
    },
    'Tirpitz': {
        'stator': {'wiring': "KZROUQHYAIGBLWVSTDXFPNMCJE"},
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
        'rotor_n': 3,
        'reflectors': (
            {'label': 'UKW', 'wiring': "GEKPBTAUMOCNILJDXZYFHWVQSR"},
        ),
        'rotatable_ref': True,
        'letter_group': 5,
        'plugboard': False
    }
}


class Plugboard:
    def __init__(self, pairs=None):
        self._pairs = {}
        self.pairs(pairs)

    def pairs(self, pairs=None):
        """
        Sets plugboard pairs to the supplied pairs
        :param pairs: {["AB", "CD", ...]} list of pairs of letters (either as strings or sublists with 2 chars)
                      where each letter can only be used once
        :return: {dict} dictionary with pairs usable by the plugboard
        """
        if pairs is not None:
            result_pairs = {}

            if pairs is None:
                return {}

            for pair in pairs:
                a, b = pair
                result_pairs[a] = b
                result_pairs[b] = a

            self._pairs = result_pairs
        else:
            pairs = []
            for pair in self._pairs.items():
                if pair[::-1] not in pairs and all(pair):
                    pairs.append(pair)
            return pairs

    def route(self, letter):
        """
        Routes letter trough the wiring pair (if the letter is wired), otherwise returns the same letter
        :param letter: {char} input letter
        :return: {char} output routed letter
        """
        return self._pairs.get(letter, letter)


class _Component:  # Base component
    def __init__(self, label, wiring):
        self._label = label
        self._wiring = wiring
        # TODO: Monkeypatch forward and backward?

    def _forward(self, letter):
        return self._wiring[alphabet.index(letter)]
    
    def _backward(self, letter):
        return alphabet[self._wiring.index(letter)]


class Stator(_Component):
    def __init__(self, wiring):
        """
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        super().__init__('ETW', wiring)

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


class Reflector(_Rotatable):
    def __init__(self, label, wiring, rotatable=False):
        super().__init__(label, wiring)

        self.__rotatable = False

    def reflect(self, letter):
        """
        Reflects letter sending it backwards into the 3 rotors
        :param letter: {char}
        :return: {char}
        """
        return super()._forward(letter)
    
    def offset(self, offset=None):
        assert self.__rotatable, "Non-rotatable reflectors don't have offset!"
        super().offset(offset)

    def position(self, numeric=False):
        """
        Returns current position (adjusted for ringstellung)
        :param numeric: {bool} whether or not the position should be numeric (02) for a letter (B)
        :return:
        """
        return "%02d" % (self.offset + 1) if numeric else alphabet[self.offset]


class Rotor(_Rotatable):
    def __init__(self, label, wiring, turnover=None):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        super().__init__(label, wiring)

        self._turnover = turnover
        self._ring_offset = 0  # "Ringstellung"
        self._turnover = turnover

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
        relative_result = super()._backward(elf.wiring.index(relative_input), True)
        return alphabet[relative_result]

    def apply_offset(self, i, negate=False):
        """
        Applies either positive or negative offset to a value
        :param i: {int} incoming position
        :param negate: {bool} subtract the offset rather than add
        :return: {int} the offset value
        """
        offset = (self._offset - self._ring_offset) % 26
        offset = -offset if negate else offset
        return (i + offset) % 26  # The alphabet has 27 - 1 letters (and index is counted from 0)

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset. There are 26 letters in the
        alphabet so 26 is the max index!
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        self._offset = (self._offset + offset_by) % 26

    def set_ring(self, setting):
        """
        Sets "Rinstellung" (ring settings) which can be misaligned with internal wiring
        :param setting: {int} new ring setting
        """
        self._ring_offset = setting % 26


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
        self.rotors = rotors
        self._stator = stator
        self._plugboard = Plugboard(plug_pairs)
        self._uhr = None

    def connect_uhr(self):
        self._uhr = Uhr()
    
    def disconnect_uhr(self):
        del self._uhr
        self._uhr = None

    def uhr_position(self, new_position=None):
        assert self._uhr is not None, "Can't set uhr position - uhr not connected!"
        if new_position is not None:
            self._uhr.position(new_position)
        else:
            return self._uhr.position()
    
    def step_rotors(self):
        """Advance rotor positions, the fourth rotor is not included because
        it never rotates"""
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
        return [rotor.ring_offset+1 for rotor in self.rotors]

    @ring_settings.setter
    def ring_settings(self, new_ring_settings):
        """
        Returns rotor positions, internal ring settings are different than the
        real ones! (01 in normal notation is 00 in internal notation)
        :param new_ring_settings: {[int, int, int]} new ring settings
        """
        for setting, rotor in zip(new_ring_settings, self.rotors):
            rotor.set_ring(setting-1)

    def press_key(self, key):
        """
        Simulates effects of pressing an Enigma keys (returning the routed
        result)
        :param key: {char} letter to encrypt
        """
        if self._uhr is not None:
            router = self._uhr
        else:
            router = self._plugboard

        self.step_rotors()

        output = router.route(key)  #self._plugboard.route(key)
        output = self._stator.forward(output)

        for rotor in reversed(self.rotors):
            output = rotor.forward(output)
        
        output = self._reflector.reflect(output)

        for rotor in self.rotors:
            output = rotor.backward(output)

        output = self._stator.backward(output)
        output = router.route(output)# self._plugboard.route(output)

        return output

    @property
    def plug_pairs(self):
        if self._uhr is not None:
            return self._uhr.pairs()
        else:
            return self._plugboard.pairs()

    @plug_pairs.setter
    def plug_pairs(self, new_plug_pairs):
        if self._uhr is not None:
            self._uhr.pairs(new_plug_pairs)
        else:
            self._plugboard.pairs(new_plug_pairs)

