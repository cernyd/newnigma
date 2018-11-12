#!/usr/bin/env python3


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
ETW = {'label': 'ETW', 'back_board': alphabet}
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
        'stator' : ETW,
        'rotors': (I, II, III, IV, V),
        'reflectors': (
            {'label': 'UKW-A', 'wiring': "EJMZALYXVBWFCRQUONTSPIKHGD"}, UKW_B, UKW_C
        )
    },
    'EnigmaM3': {
        'stator' : ETW,
        'rotors': (I, II, III, IV, V, VI, VII, VIII),
        'reflectors': (UKW_B, UKW_C)
    },
    'EnigmaM4': {
        'stator' : ETW,
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
        'stator' : ETW,
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
        'stator' : ETW_QWERTZ,
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
        'stator' : ETW_QWERTZ,
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
        'stator' : {'label': 'ETW', 'back_board': "KZROUQHYAIGBLWVSTDXFPNMCJE"},
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


class Enigma:
    def __init__(self, reflector, rotors, stator):
        """
        :param reflector: {components.Reflector}
        :param rotors: {[Rotor, Rotor, Rotor, ...]} rotor count depends on model
        :param stator: {Stator}
        """
        self.reflector = reflector
        self.rotors = rotors
        self.stator = stator

    def step_rotors(self, n):
        """
        :param n: {int} how many times to step
        """
        step_next = False

        # TODO: Step primary rotor, double stepper effect?

    def button_press(self, letter):
        """
        :param letter: {char}
        :return: {char}
        """


# TODO: Decide whether or not it is beneficial to pursue the DRY principle at all costs

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
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, letter):
        return self.wiring[alphabet.index(letter)]


class Rotor:
    def __init__(self, label, wiring):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param wiring: {str} defines the way letters are routed trough the rotor
        """
        self.wiring = [alphabet.index(letter) for letter in wiring]

        self.label = label
        self.offset = 0  # "Stellung"
        self.ring_offset = 0  # "Ringstellung"

    def forward(self, letter):
        """
        Routes the letter from the front board to the back board
        :param letter: {char}
        :return: {char}
        """
        relative_result = self.wiring[self.apply_offset(alphabet.index(letter))]
        return alphabet[self.apply_offset(relative_result)]

    def backward(self, letter):
        """
        Routes the letter from the back board to the front board
        :param letter: {char}
        :return: {char}
        """
        relative_input = self.apply_offset(alphabet.index(letter), True)
        return alphabet[self.apply_offset(self.wiring.index(relative_input), True)]

    def apply_offset(self, i, negate=False):
        """
        Applies either positive or negative offset to a value
        :param i: {int}
        :param negate: {bool} subtract the offset rather than add
        :return: {int} the offset value
        """
        offset = -self.offset if negate else self.offset
        return (i + offset) % 26  # The alphabet has 27 - 1 letters (and index is counted from 0)

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset. There are 26 letters in the
        alphabet so 26 is the max index!
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        self.offset = (self.offset + offset_by) % 26

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
        shown_position = (self.offset + self.ring_offset) % 26
        return "%02d" % (shown_position + 1) if numeric else alphabet[shown_position]
