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
ETW_QWERTZ = {'back_board': "QWERTZUIOASDFGHJKPYXCVBNML"}

# Rotors
I = {'label': 'I', 'back_board': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'turnover': 'Q'}
II = {'label': 'II', 'back_board': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'turnover': 'E'}
III = {'label': 'III', 'back_board': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'turnover': 'V'}
IV = {'label': 'IV', 'back_board': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'turnover': 'J'}
V = {'label': 'V', 'back_board': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'turnover': 'Z'}
VI = {'label': 'VI', 'back_board': 'JPGVOUMFYQBENHZRDKASXLICTW', 'turnover': 'ZM'}
VII = {'label': 'VII', 'back_board': 'NZJHGRCXMYSWBOUFAIVLPEKQDT', 'turnover': 'ZM'}
VIII = {'label': 'VIII', 'back_board': 'FKQHTLXOCBJSPDZRAMEWNIUYGV', 'turnover': 'ZM'}


# Reflectors
UKW_B = {'label': 'UKW-B', 'back_board': "YRUHQSLDPXNGOKMIEBFZCWVJAT"}
UKW_C = {'label': 'UKW-C', 'back_board': "FVPJIAOYEDRZXWGCTKUQSBNMHL"}


# Enigma D and K
ENIGMA_D_K = {
    'stator' : ETW_QWERTZ,
    'rotors': (
        {'label': 'I', 'back_board': 'LPGSZMHAEOQKVXRFYBUTNICJDW', 'turnover': 'Y'},
        {'label': 'II', 'back_board': 'SLVGBTFXJQOHEWIRZYAMKPCNDU', 'turnover': 'E'},
        {'label': 'III', 'back_board': 'CJGDPSHKTURAWZXFMYNQOBVLIE', 'turnover': 'N'},
    ),
    'reflectors': (
        {'label': 'UKW', 'back_board': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
    )
}


historical_data = {
    'Enigma1': {
        'stator' : ETW,
        'rotors': (I, II, III, IV, V),
        'reflectors': (
            {'label': 'UKW-A', 'back_board': "EJMZALYXVBWFCRQUONTSPIKHGD"}, UKW_B, UKW_C
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
            {'label': 'Beta', 'back_board': 'LEYJVCNIXWPBQMDRTAKZGFUHOS'},
            {'label': 'Gamma', 'back_board': 'FSOKANUERHMBTIYCWLQPZXVGJD'}
        ),
        'reflectors': (
            {'label': 'UKW-b', 'back_board': "ENKQAUYWJICOPBLMDXZVFTHRGS"},
            {'label': 'UKW-c', 'back_board': "RDOBJNTKVEHMLFCWZAXGYIPSUQ"}
        )
    },
    'Norenigma': {
        'stator' : ETW,
        'rotors': (
            {'label': 'I', 'back_board': 'WTOKASUYVRBXJHQCPZEFMDINLG', 'turnover': 'Q'},
            {'label': 'II', 'back_board': 'GJLPUBSWEMCTQVHXAOFZDRKYNI', 'turnover': 'E'},
            {'label': 'III', 'back_board': 'JWFMHNBPUSDYTIXVZGRQLAOEKC', 'turnover': 'V'},
            {'label': 'IV', 'back_board': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'turnover': 'J'},
            {'label': 'V', 'back_board': 'HEJXQOTZBVFDASCILWPGYNMURK', 'turnover': 'Z'}
        ),
        'reflectors': (
            {'label': 'UKW', 'back_board': "MOWJYPUXNDSRAIBFVLKZGQCHET"},
        )
    },
    'EnigmaG': {
        'stator' : ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'back_board': 'LPGSZMHAEOQKVXRFYBUTNICJDW', 'turnover': 'SUVWZABCEFGIKLOPQ'},
            {'label': 'II', 'back_board': 'SLVGBTFXJQOHEWIRZYAMKPCNDU', 'turnover': 'STVYZACDFGHKMNQ'},
            {'label': 'III', 'back_board': 'CJGDPSHKTURAWZXFMYNQOBVLIE', 'turnover': 'UWXAEFHKMNR'},
        ),
        'reflectors': (
            {'label': 'UKW', 'back_board': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        )
    },
    'EnigmaD': ENIGMA_D_K,
    'EnigmaK': ENIGMA_D_K,
    'SwissK': {
        'stator' : ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'back_board': 'PEZUOHXSCVFMTBGLRINQJWAYDK', 'turnover': 'Y'},
            {'label': 'II', 'back_board': 'ZOUESYDKFWPCIQXHMVBLGNJRAT', 'turnover': 'E'},
            {'label': 'III', 'back_board': 'EHRVXGAOBQUSIMZFLYNWKTPDJC', 'turnover': 'N'},
        ),
        'reflectors': (
            {'label': 'UKW', 'back_board': "IMETCGFRAYSQBZXWLHKDVUPOJN"},
        )
    },
    'Railway': {
        'stator' : ETW_QWERTZ,
        'rotors': (
            {'label': 'I', 'back_board': 'JGDQOXUSCAMIFRVTPNEWKBLZYH', 'turnover': 'N'},
            {'label': 'II', 'back_board': 'NTZPSFBOKMWRCJDIVLAEYUXHGQ', 'turnover': 'E'},
            {'label': 'III', 'back_board': 'JVIUBHTCDYAKEQZPOSGXNRMWFL', 'turnover': 'Y'},
        ),
        'reflectors': (
            {'label': 'UKW', 'back_board': "QYHOGNECVPUZTFDJAXWMKISRBL"},
        )
    },
    'Tirpitz': {
        'stator' : {'label': 'ETW', 'back_board': "KZROUQHYAIGBLWVSTDXFPNMCJE"},
        'rotors': (
            {'label': 'I', 'back_board': 'KPTYUELOCVGRFQDANJMBSWHZXI', 'turnover': 'WZEKQ'},
            {'label': 'II', 'back_board': 'UPHZLWEQMTDJXCAKSOIGVBYFNR', 'turnover': 'WZFLR'},
            {'label': 'III', 'back_board': 'QUDLYRFEKONVZAXWHMGPJBSICT', 'turnover': 'WZEKQ'},
            {'label': 'IV', 'back_board': 'CIWTBKXNRESPFLYDAGVHQUOJZM', 'turnover': 'WZFLR'},
            {'label': 'V', 'back_board': 'UAXGISNJBVERDYLFZWTPCKOHMQ', 'turnover': 'YCFKR'},
            {'label': 'VI', 'back_board': 'XFUZGALVHCNYSEWQTDMRBKPIOJ', 'turnover': 'XEIMQ'},
            {'label': 'VII', 'back_board': 'BJVFTXPLNAYOZIKWGDQERUCHSM', 'turnover': 'YCFKR'},
            {'label': 'VIII', 'back_board': 'YMTPNZHWKODAJXELUQVGCBISFR', 'turnover': 'XEIMQ'}
        ),
        'reflectors': (
            {'label': 'UKW', 'back_board': "GEKPBTAUMOCNILJDXZYFHWVQSR"},
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


class _RotorBase:
    def __init__(self, label, back_board):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param back_board: {str} defines the way letters are routed trough the rotor
        """
        self.label = label

        # Pairs of letters FRONT <-> BACK
        self.wiring = [alphabet.index(letter) for letter in back_board]
        self.offset = 0

    def _route_forward(self, letter):
        """
        Routes the letter from the front board to the back board
        :param letter: {char}
        :return: {char}
        """
        relative_input = (alphabet.index(letter) + self.offset) % 26
        print("Rel input: " + str(relative_input))
        relative_result = self.wiring[relative_input]
        absolute_result = (relative_result + self.offset) % 26
        return alphabet[absolute_result]


    def _route_backward(self, letter):
        """
        Routes the letter from the back board to the front board
        :param letter: {char}
        :return: {char}
        """
        relative_input = (alphabet.index(letter) - self.offset) % 26
        relative_result = self.wiring.index(relative_input)
        absolute_result = (relative_result - self.offset) % 26
        return alphabet[absolute_result]

    def rotate(self, offset_by=1):
        """
        Calculates new rotor offset based on input offset
        :param offset_by: {int} how many places the rotor should be offset
                          (offset_by > 0 = rotate forwards; offset_by < 0 = rotate backwards)
        """
        print("Before: %d" % self.offset)
        self.offset = (self.offset + offset_by) % 26
        print("After: %d" % self.offset)
        print("==================================")


class Rotor(_RotorBase):
    def __init__(self, label, back_board):
        """
        :param label: {str} rotor label (I, II, III, ...)
        :param back_board: {str} defines the way letters are routed trough the rotor
        """
        super().__init__(label, back_board)
