#!/usr/bin/env python3
"""
Copyright (C) 2016, 2017  David Cerny

This file is part of gnunigma

Gnunigma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from string import ascii_uppercase as alphabet
from itertools import permutations, chain
from cfg_handler import Config
from functools import wraps
import unittest
from tkinter import messagebox
from os import path


# UNIT TEST

class TestEnigma(unittest.TestCase):
    """Used to test if enigma class behaves like the real life counterpart"""
    model = ''
    cfg_path = []

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.cfg = Config(TestEnigma.cfg_path).data['test_cfg']
        self.subject = None
        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.yaml'])
        self.reset_subject()

    def reset_subject(self):
        self.subject = self.enigma_factory.produce_enigma('EnigmaM3')

    def test_encrypt_decrypt(self):
        """Tests if encryption and decryption are working properly"""
        buffer = self.cfg['test_encrypt_decrypt']
        for test in permutations(['encrypted', 'decrypted']):
            self.reset_subject()
            output = ''
            for letter in buffer[test[0]]:
                output += self.subject.button_press(letter)

            err_msg = 'Failed to {}!'.format(test[1][:-2])
            self.assertEqual(output, buffer[test[1]], err_msg)
        with self.assertRaises(AssertionError):
            self.subject.button_press(18)

    def test_rotors(self):
        """Tests if rotors are assigned properly"""
        self.reset_subject()
        rotors = self.cfg['test_rotors']['rotors']
        self.subject.rotors = self.enigma_factory.produce_rotor('EnigmaM3',
                                                                'rotor', rotors)
        self.assertEqual(self.subject.rotor_labels, rotors,
                         'Invalid rotor order assigned!')

    def test_positions(self):
        """Tests if rotor positions are set properly"""
        self.reset_subject()
        positions = self.cfg['test_positions']['positions']
        self.subject.positions = positions
        self.assertEqual(self.subject.positions, positions,
                         'Positions assigned in wrong order!')
        with self.assertRaises(AssertionError):
            self.subject.positions = 14651, 'garbage', -15

    def test_reflector(self):
        """Tests if the reflector is set properly"""
        self.reset_subject()
        reflector = self.cfg['test_reflector']['reflector']
        self.subject.reflector = self.enigma_factory.produce_rotor('EnigmaM3', 'reflector', reflector)
        self.assertEqual(self.subject.reflector.label, reflector,
                         'Invalid rotor assigned!')
        with self.assertRaises(AssertionError):
            self.subject.reflector = 'garbage_input'

    def test_ring_settings(self):
        """Tests if ring settings are set properly"""
        self.reset_subject()
        ring_settings = self.cfg['test_ring_settings']['ring_settings']
        self.subject.ring_settings = ring_settings
        self.assertEqual(self.subject.ring_settings, ring_settings,
                         'Invalid ring settings assigned!')
        with self.assertRaises(AssertionError):
            self.subject.ring_settings = [12, 'garbage_input', 798715]

    def test_plugboard(self):
        """Checks if plugboard pairs are set propertly"""
        self.reset_subject()
        plug_pairs = self.cfg['test_plugboard']['pairs']
        self.subject.plugboard = {'normal_pairs': plug_pairs}

        err_msg = 'Invalid plugboard pairs assigned!'
        self.assertEqual(self.subject.plugboard['normal_pairs'], plug_pairs,
                         err_msg)
        with self.assertRaises(AttributeError):
            self.subject.plugboard = 'garbage_input'


# GENERIC COMPONENTS

def join_list(lst):
    """Chains a list ( list of lists )"""
    return list(chain.from_iterable(lst))


def are_unique(pairs):
    """Checks if values in letter pairs are unique"""
    value_list = join_list(pairs)
    return len(value_list) == len(set(value_list))


class WiredPairs:
    """Returns the other letter from pairs if one letter is given.
    IS FLEXIBLE!"""
    def __init__(self, pairs=tuple()):
        self._pairs = pairs

    @property
    def pairs(self):
        """Returns letter pairs"""
        return self._pairs

    @pairs.setter
    def pairs(self, pairs):
        """Sets letter pairs"""
        assert (len(pairs) <= 13), "Invalid number of pairs!"
        assert are_unique(pairs), 'A letter can only be wired once!'

        self._pairs = pairs

    def pairs_route(self, letter):
        """Routes a letter trough letter pairs"""
        neighbour = []
        for pair in self._pairs:
            if letter in pair:
                neighbour.extend(pair)
                neighbour.remove(letter)
                return neighbour[0]
        return letter  # If no connection found


# PLUGBOARD

class Plugboard:
    """Standard and Uhr pairs can be set"""
    def __init__(self, pairs=None):
        self._wired_pairs = WiredPairs()  # Self steckered, no scrambling
        self._uhr = Uhr()  # Uhr steckered, always 10 pairs
        # Pairs are stored additionally for easier searching, WILL REMOVE LATER
        if pairs:
            self.pairs = pairs

    def uhr_letter_color(self, letter):
        """Returns plug style of the input letter"""
        for key, value in self._uhr.pairs.items():
            if letter == key:
                color = value[0]
                if 'a' in color:
                    return {'bg': 'red', 'fg': 'white'}
                elif 'b' in color:
                    return {'bg': 'gray', 'fg': 'white'}

        return {'bg': 'black', 'fg': 'white'}

    @property
    def pairs(self):
        """Returns list of all combined connected pairs"""
        return {'uhr_pairs': self._uhr.simple_pairs,
                'normal_pairs': self._wired_pairs.pairs}

    @pairs.setter
    def pairs(self, pairs):
        """Allows to set up to 13 normal pairs or 10 Uhr pairs + up to 3 normal
        pairs"""
        try:
            normal_pairs = pairs.get('normal_pairs', tuple())
            uhr_pairs = pairs.get('uhr_pairs', tuple())
        except AttributeError:
            raise AttributeError("Invalid pairs datatype!")

        err_msg = "A letter can only be wired once!"
        assert are_unique(list(list(normal_pairs) + list(uhr_pairs))), err_msg

        if uhr_pairs:
            self._uhr.pairs = uhr_pairs
        self._wired_pairs.pairs = normal_pairs

    def clear_pairs(self):
        """Clears all plugboard pairs ( normal and uhr pairs )"""
        self._wired_pairs.pairs = tuple()
        self._uhr.pairs = tuple()

    def route(self, letter):
        """Routes letter either with Uhr or with normal pairs"""
        if letter in join_list(self._uhr.simple_pairs):
            return self._uhr.route(letter)
        else:
            return self._wired_pairs.pairs_route(letter)

    @property
    def uhr_connected(self):
        """Checks if the uhr is connected"""
        return len(self._uhr.simple_pairs) != 0

    @property
    def uhr_position(self):
        """Returns current uhr position"""
        return self._uhr.position

    @uhr_position.setter
    def uhr_position(self, position):
        """Sets uhr position"""
        self._uhr.position = position


# ENIGMA MODELS

class EnigmaFactory:
    """Factory for producing enigma machines ( initialised more simply by
    choosing defaults from available config ), Can create rotor objects too"""
    def __init__(self, cfg_path):
        self.cfg = Config(cfg_path)

    @staticmethod
    def _get_model_class(model):
        """Attempts to get object based on input name"""
        try:
            return globals()[model]
        except KeyError:
            print("No enigma model found for \"{}\"! "\
                  "Attempting to return alternative object...".format(model))
            return Enigma1

    def _get_model_data(self, model, rotor_count, reflector=None, rotors=None, stator=None):
        """Gets default configuration data, custom preferences can override default
        data."""
        model_data = self.model_data(model)

        # Generates default data if default parameters not overridden
        if not reflector:
            reflector = model_data['reflectors'][0]
        if not rotors:
            rotors = model_data['rotors'][:rotor_count]
        if not stator:
            stator = model_data['stators'][0]

        reflector = self.produce_rotor(model, 'reflector', reflector)
        rotors = self.produce_rotor(model, 'rotor', rotors)
        stator = self.produce_rotor(model, 'stator', stator)

        return reflector, rotors, stator, model_data

    def all_models(self):
        """Returns all enigma models as a string list"""
        returns = []
        for key in self.cfg.data.keys():
            if key not in ['labels', 'layout']:
                returns.append(key)

        return returns

    def produce_enigma(self, model, reflector=None, rotors=None, stator=None,
                       master=None, reflector_pairs=tuple()):
        """Produces an enigma machine given a specific model ( must be available
        in the specified cfg_path )"""
        ModelClass = self._get_model_class(model)
        data = self._get_model_data(model, ModelClass.rotor_count, reflector,
                                    rotors, stator)

        if master:
            class TkEnigma(ModelClass):
                """Enigma adjusted for Tk rotor lock,
                    ignore the property signatures please..."""
                def __init__(self, master, enigma_factory, *data):
                    self._enigma_factory = enigma_factory
                    ModelClass.__init__(self, *data)
                    self.master = master

                def button_press(self, letter):
                    return ModelClass.button_press(self, letter)

                def step_primary(self, places=1):
                    if not self.master.rotor_lock:
                        ModelClass.step_primary(self, places)

                @ModelClass.reflector.setter
                def reflector(self, reflector):
                    try:
                        if type(reflector) == str:
                            new_reflector = self._enigma_factory.produce_rotor(
                                model, 'reflector', reflector)
                            ModelClass.reflector.fset(self, new_reflector)
                        else:
                            ModelClass.reflector.fset(self, reflector)
                    except AttributeError:
                        messagebox.showwarning('Invalid reflector',
                                               'Invalid reflector,'
                                               ' please try '
                                               'again...')

                @ModelClass.rotors.setter
                def rotors(self, rotors):
                    """Adds a visual error feedback ( used only in the
                    tk implementation )"""
                    try:
                        if type(rotors[0]) == str:
                            new_rotors = self._enigma_factory.produce_rotor(model, 'rotor', rotors)
                            ModelClass.rotors.fset(self, new_rotors)
                        else:
                            ModelClass.rotors.fset(self, rotors)
                    except AttributeError:
                        messagebox.showwarning('Invalid rotor',
                                               'Some of rotors are not \n'
                                               'valid, please try again...')

            return TkEnigma(master, self, *data, reflector_pairs)
        else:
            return ModelClass(*data)

    def produce_rotor(self, model, rotor_type, labels):
        """Creates and returns new object based on input"""
        if labels == ['UKW-D'] or labels == 'UKW-D':
            return UKWD()


        cfg = self.cfg.data[model][rotor_type+'s']
        return_rotors = []

        if type(labels) != list and type(labels) != tuple:
            labels = [labels]

        for label in labels:
            curr_cfg = None
            match = False
            for item, config in cfg.items():
                if item == label:
                    curr_cfg = config
                    curr_cfg['label'] = item
                    match = True
                    break

            assert match, "No configuration found for label \"{}\"!".format(label)

            if rotor_type == 'rotor':
                return_rotors.append(Rotor(**curr_cfg))
            elif rotor_type == 'reflector':
                return_rotors.append(Reflector(**curr_cfg))
            elif rotor_type == 'stator':
                return_rotors.append(Stator(**curr_cfg))

        if len(return_rotors) == 1:
            return return_rotors[0]
        return return_rotors

    def model_data(self, model):
        """Returns all available rotor labels for the selected enigma model"""
        model_data = {'model': model,
                      'labels': self.cfg.data['labels'],
                      'layout': self.cfg.data['layout']
                      }

        for item in 'reflectors', 'rotors', 'stators':
            model_data[item] = list(self.cfg.data[model][item].keys())

        return model_data


class Enigma:
    """Base for all enigma objects, has no plugboard, default rotor count for
    all enigma machines is 3."""
    rotor_count = 3
    has_plugboard = False

    def __init__(self, reflector, rotors, stator, factory_data=None,
                 reflector_pairs=tuple()):
        self._stator = stator
        self._reflector = None
        self._rotors = None
        self.reflector = reflector
        self.rotors = rotors
        self.factory_data = factory_data  # All available components
        if reflector_pairs:
            self.reflector_pairs = reflector_pairs

    def step_primary(self, places):
        """Steps primary rotor, other rotors will step too if in appropriate
        positions."""
        step_next = False
        index = 0
        for rotor in reversed(self._rotors):
            if index == 0:
                if places < 0:
                    rotor.rotate(places)
                if rotor.position in rotor.turnover:
                    step_next = True
                if places > 0:
                    rotor.rotate(places)
            elif index == 1 and rotor.position in rotor.turnover:
                rotor.rotate(places)
                step_next = True
            elif step_next:
                rotor.rotate(places)
                step_next = False

            index += 1

    @property
    def reflector_pairs(self):
        """Returns reflector pairs if UKW-D is connected"""
        if self._reflector.label == 'UKW-D':
            return self.reflector.wiring_pairs
        return ()

    @reflector_pairs.setter
    def reflector_pairs(self, wiring_pairs):
        """Sets reflector pairs if the UKW-D is currently being used"""
        if self._reflector.label == 'UKW-D':
            self.reflector.wiring_pairs = wiring_pairs

    @property
    def rotor_labels(self):
        """Returns rotor type ( label ), for the rotor order window."""
        return [rotor.label for rotor in self._rotors]

    @property
    def rotors(self):
        """Returns current rotors"""
        return self._rotors

    @rotors.setter
    def rotors(self, rotors):
        """Sets rotors"""
        for rotor in rotors:
            assert isinstance(rotor, (Rotor, Luckenfuller)), "Invalid rotor class of \"{}\"!".format(type(rotor).__name__)
        assert len(rotors) == self.rotor_count, "Invalid number of rotors!"
        self._rotors = rotors

    @property
    def positions(self):
        """Returns current rotor positions"""
        return [rotor.position for rotor in self._rotors]

    @positions.setter
    def positions(self, positions):
        """Sets rotor positions"""
        for position, rotor in zip(positions, self._rotors):
            rotor.position = position

    @property
    def reflector(self):
        """Returns current reflector object"""
        return self._reflector

    @reflector.setter
    def reflector(self, reflector):
        """Sets current reflector"""
        assert isinstance(reflector, (Reflector, UKWD)), "Invalid rotor class of \"{}\"!".format(type(reflector).__name__)
        self._reflector = reflector

    @property
    def ring_settings(self):
        """Returns ring settings"""
        return [rotor.ring_setting for rotor in self.rotors]

    @ring_settings.setter
    def ring_settings(self, offsets):
        """Sets rotor ring settings"""
        for rotor, setting in zip(self.rotors, offsets):
            rotor.ring_setting = setting

    def button_press(self, letter):
        """Simulates an enigma button press including rotor stepping"""
        self.step_primary(1)

        output = self._stator.forward(letter)

        for rotor in reversed(self._rotors):
            output = rotor.forward(output)

        output = self.reflector.reflect(output)

        for rotor in self._rotors:
            output = rotor.backward(output)

        return self._stator.backward(output)

    def dump_config(self):
        """Dumps the whole enigma data config"""
        data = dict(reflector=self.reflector.label,
                    rotors=self.rotor_labels,
                    rotor_positions=self.positions,
                    ring_settings=self.ring_settings,
                    model=self.factory_data['model'])

        if self.reflector.label == 'UKW-D':
            data['reflector_pairs'] = ' '.join(self.reflector.wiring_pairs)

        return data


class Enigma1(Enigma):
    """Adds plugboard functionality, compatible with all EnigmaM_ models
    except M4 ( Four rotors )"""
    has_plugboard = True

    def __init__(self, reflector, rotors, stator, factory_data,
                 normal_pairs=tuple(), uhr_pairs=tuple()):
        Enigma.__init__(self, reflector, rotors, stator, factory_data)
        self._plugboard = Plugboard({'normal_pairs': normal_pairs,
                                     'uhr_pairs': uhr_pairs})

    @property
    def uhr_position(self):
        """Returns current uhr position"""
        return self._plugboard.uhr_position

    @uhr_position.setter
    def uhr_position(self, position):
        """Sets uhr position"""
        self._plugboard.uhr_position = position

    @property
    def uhr_connected(self):
        """Returns True if uhr is connected"""
        return self._plugboard.uhr_connected

    def uhr_letter_color(self, letter):
        return self._plugboard.uhr_letter_color(letter)

    @property
    def plugboard(self):
        """Plugboard routing pairs"""
        return self._plugboard.pairs

    @plugboard.setter
    def plugboard(self, pairs):
        """Sets plugboard pairs"""
        self._plugboard.pairs = pairs

    def clear_plugboard(self):
        """Clears all pairs on the plugboard"""
        self._plugboard.clear_pairs()

    def button_press(self, letter):
        """Wraps the base enigma routing with plugboard"""
        output = self._plugboard.route(letter)
        output = Enigma.button_press(self, output)
        return self._plugboard.route(output)

    def dump_config(self):
        """Returns enigma state ( rotors, positions, plug pairs, etc... )"""
        config = Enigma.dump_config(self)
        normal_pairs = self._plugboard.pairs['normal_pairs']
        uhr_pairs = self._plugboard.pairs['uhr_pairs']
        config.update(normal_pairs=normal_pairs, uhr_pairs=uhr_pairs,
                      uhr_position=str(self._plugboard.uhr_position))
        return config


class Norenigma(Enigma):
    """Enigma model used in Norway"""


class EnigmaG(Enigma):
    """Zahlwerk Enigma with a cog mechanism."""


class EnigmaD(Enigma):
    """First Enigma with removable rotors, successor of Enigma C"""


class SwissK(Enigma):
    """Used in Switzerland"""


class Railway(Enigma):
    """Used by german Reichsbahn"""


class EnigmaK(EnigmaD):
    """Functionally identical to Enigma D"""


class Tirpitz(EnigmaK):
    """Used by the Japanese"""


class EnigmaM3(Enigma1):
    """Name for the group of Enigma M1, M2 and M3 machines. All of them are
    practically identical"""


class EnigmaM4(EnigmaM3):
    """Navy version with four rotors, otherwise identical, UKW-D can be used
    instead. Thin reflectors are used, UKW-D can be used too if the extra rotor
    and thin reflector are replaced."""
    rotor_count = 4

    @EnigmaM3.reflector.setter
    def reflector(self, reflector):
        """Reflector setting is wrapped with automatic removal of extra rotor
        in EnigmaM4"""
        EnigmaM3.reflector.fset(self, reflector)

        if reflector.label == 'UKW-D' and self.rotor_count == 4:
            self.rotor_count = 3
            if self.rotors:
                self.removed_rotor = self._rotors.pop(0)
            self._reflector = reflector
        elif reflector.label != 'UKW-D':
            self.rotor_count = 4
            if self.rotors:
                if len(self.rotors) == 3:
                    self.rotors = [self.removed_rotor] + self.rotors


# ROTOR COMPONENTS

class _RotorBase:
    """Base class for Rotors and Reflectors"""
    def __init__(self, label, back_board):
        """All parameters except should be passed in **config"""

        self.back_board = back_board  # Defines internal wiring
        self.label = label

    def _check_input(func):
        """Checks if the rotor is given correct input ( a single letter for the
        alphabet )"""
        @wraps(func)
        def wrapper(self, letter):
            letter = str(letter).upper()

            if letter not in alphabet:
                raise AssertionError(
                    "Input \"{}\" not single a letter!".format(str(letter)))

            elif len(letter) != 1:
                raise AssertionError("Length o \"{}\" is not 1!").format(str(letter))

            return func(self, letter)

        return wrapper

    def _route_forward(self, letter):
        """Routes letters from front board to back board"""
        return self.back_board[alphabet.index(letter)]


class _Rotatable:
    """Adds the ability to change board offsets"""
    def _change_board_offset(self, board, places=1):
        """Changes offset of a specified board."""
        old_val = getattr(self, board)
        new_val = old_val[places:] + old_val[:places]
        setattr(self, board, new_val)


class Reflector(_RotorBase):
    """Reflector class, used to """
    @_RotorBase._check_input
    def reflect(self, letter):
        """Reflects letter back"""
        return self._route_forward(letter)


class Stator(_RotorBase):
    @_RotorBase._check_input
    def forward(self, letter):
        """Routes letter from front to back"""
        return self._route_forward(letter)

    @_RotorBase._check_input
    def backward(self, letter):
        """Routes letter from back to front"""
        return alphabet[self.back_board.index(letter)]


class Rotor(Stator, _Rotatable):
    """Inherited from RotorBase, adds rotation and ring setting functionality"""
    def __init__(self, label,  back_board, turnover=''):
        Stator.__init__(self, label, back_board)
        self._turnover = turnover  # Letter shown on turnover position

        # position_ring = position currently shown in the position window,
        # relative_board = used in the actual wiring ( internal, between
        # position rings )
        self.position_ring, self.relative_board = [alphabet] * 2

    def _compensate(func):
        """Converts input to relative input and
        relative output to absolute output, does some assertions too."""
        @wraps(func)
        def wrapper(self, letter):
            relative_input = self.relative_board[alphabet.index(letter)]
            return alphabet[
                self.relative_board.index(func(self, relative_input))]
        return wrapper

    @_compensate
    def forward(self, letter):
        """Routes a letter ( an electrical signal ) from right to left ( or
        front to back side )"""
        return Stator.forward(self, letter)

    @_compensate
    def backward(self, letter):
        """Routes a letter ( an electrical signal ) from left to right ( or
        back to front side )"""
        return Stator.backward(self, letter)

    def rotate(self, places=1):
        """Rotates rotor by one x places, returns True if the next rotor should
        be turned over"""
        for board in 'relative_board', 'position_ring':
            self._change_board_offset(board, places)

    @property
    def turnover(self):
        """Returns current turnover"""
        return self._turnover

    @property
    def position(self):
        """Returns rotor position"""
        return self.position_ring[0]

    @position.setter
    def position(self, position):
        """Sets rotor to target position"""
        self._generic_setter("Invalid position\"%s\"!",
                             lambda: getattr(self, 'position'), position, self.rotate)

    @staticmethod
    def _generic_setter(message, uptodate_value, target_value, update_action):
        """Can be used to rotate any iterable"""
        assert str(target_value) in alphabet, message % str(target_value)
        while uptodate_value() != target_value:
            update_action()

    @property
    def ring_setting(self):
        """Returns ring setting"""
        return self.position_ring[self.relative_board.index('A')]

    @ring_setting.setter
    def ring_setting(self, setting):
        """Sets rotor indicator offset relative to the internal wiring"""
        self._generic_setter("Invalid ring setting \"%s\"!",
                             lambda: getattr(self, 'ring_setting'), setting,
                             lambda: self._change_board_offset('relative_board'))


# HISTORICAL ENIGMA PECULIARITIES

class Luckenfuller(Rotor):
    """Rotor with adjustable turnover notches. This object is not included in
    the official enigma gui because it was never used in reality"""
    def __init__(self, label, back_board, turnover):
        Rotor.__init__(self, label, back_board, turnover)

    @Rotor.turnover.setter
    def turnover(self, turnover):
        """Turnover can be set in luckenfullers"""
        self._turnover = turnover


class UKWD:
    """Could be used in 3 rotor enigma versions, mostly used in EnigmaM4
    ( replacing the thin reflector and extra rotor! ). UKW-D is a field
    rewirable Enigma machine reflector."""
    def __init__(self, pairs=('AB', 'CD', 'EF', 'GH', 'IK', 'LM', 'NO', 'PQ',
                              'RS', 'TU', 'VW', 'XZ')):
        self._pairs = WiredPairs(('BO', ))  # BO pair is static!
        self.german_notation = 'AZXWVUTSRQPONMLKIHGFEDCB'
        self.actual_letters = 'ACDEFGHIJKLMNPQRSTUVWXYZ'
        self.wiring_pairs = pairs
        self.label = 'UKW-D'

    @property
    def wiring_pairs(self):
        """Wiring pairs of the reflector"""
        return_pairs = []

        for pair in self._pairs.pairs:
            pair = ''.join(pair)
            if pair != 'BO' and pair != 'OB':
                curr_pair = ''
                for letter in pair:
                    curr_pair += self._to_german_notation(letter)
                return_pairs.append(curr_pair)

        return return_pairs

    def _to_actual_letter(self, letter):
        """Transfers letter to actual wiring"""
        return self.actual_letters[self.german_notation.index(letter)]

    def _to_german_notation(self, letter):
        """Transfers actual wiring to german notation ( on pair read )"""
        return self.german_notation[self.actual_letters.index(letter)]

    @wiring_pairs.setter
    def wiring_pairs(self, pairs):
        """Sets up wiring pairs, BO is static!
        ( will appear as 'JY' while setting)"""
        assert len(pairs) == 12, "Invalid number of pairs, " \
                                 "only number of pairs possible is 12!"

        all_letters = join_list(pairs)
        assert 'J' not in all_letters and 'Y' not in all_letters, \
            "The 'JY' pair is hardwired and can not be rewired"

        new_pairs = ['BO']
        for pair in pairs:
            pair = ''.join(pair)
            if pair != 'BO' and pair != 'OB':
                curr_pair = ''
                for letter in pair:
                    curr_pair += self._to_actual_letter(letter)
                new_pairs.append(curr_pair)

        self._pairs.pairs = new_pairs

    def reflect(self, letter):
        """Reflects letter like a standard reflector"""
        return self._pairs.pairs_route(letter)


class Uhr(_Rotatable):
    """Uhr is an enigma machine extension, allows the plugboard to be scrambled
    based on a key, every 4th position starting with 00 is reciprocal, maximum
    position is 40. All other positions are not reciprocal ( encryption is not
    directly reversible: A > B, B > X ( not A! )."""
    def __init__(self, pairs=''):
        """On position 00, all bx cables are connected to corresponding ax
        cables. Position 00 is reciprocal and allows communication with non-uhr
        users."""
        self.back_board = [26, 11, 24, 21, 2, 31, 0, 25, 30, 39, 28, 13, 22, 35,
                           20, 37, 6, 23, 4, 33, 34, 19, 32, 9, 18, 7, 16, 17,
                           10, 3, 8, 1, 38, 27, 36, 29, 14, 15, 12, 5]

        self.relative_board = tuple(range(40))
        # Relative and indicator boards are the same because Uhr did not have turnovers

        # Number pairs stand for ( SEND, RECEIVE )
        # WARNING - These positions are absolute, only the wiring disk has offset
        self._black_red_plug_pairs = {'1a': (0, 2), '1b': (4, 6),
                                      '2a': (4, 6), '2b': (16, 18),
                                      '3a': (8, 10), '3b': (28, 30),
                                      '4a': (12, 14), '4b': (36, 38),
                                      '5a': (16, 18), '5b': (24, 26),
                                      '6a': (20, 22), '6b': (12, 14),
                                      '7a': (24, 26), '7b': (0, 2),
                                      '8a': (28, 30), '8b': (8, 10),
                                      '9a': (32, 34), '9b': (20, 22),
                                      '10a': (36, 38), '10b': (32, 34)}

        self._pairs = {}
        self._simple_pairs = []
        self.pairs = pairs

    @property
    def simple_pairs(self):
        """Returns simple representation of pairs ( only letters )"""
        return tuple(self._simple_pairs)

    @property
    def pairs(self):
        """Returns full representation of pairs ( plug numbers, colors... )"""
        return self._pairs

    @pairs.setter
    def pairs(self, pairs):
        """
        Uhr has exacly 10 pairs of wires because it was the standard number of
        plugboard connections during the war ( mathematically optimal number,
        increases the possible pair number greatly in combinatorics )
        1 pair: 325
        2 pairs: 44.850
        3 pairs: 3,453,450
        4 pairs: 164,038,875
        5 pairs: 5,019,589,575
        6 pairs: 100,391,791,500
        7 pairs: 1,305,093,289,500
        8 pairs: 10,767.019,638,375
        9 pairs: 58,835.098,191,875
        10 pairs: 150,738,274,937,250
        11 pairs: 205,552,193,096,250
        12 pairs: 102,776,096,548,125
        13 pairs: 7,905,853,580,625
        """

        if len(pairs) > 0:
            err_msg = """All 10 pairs must be wired, otherwise the electrical
                     signal could be lost during non-reciprocal substitution."""

            assert (len(pairs) == 10), err_msg

            assert are_unique(pairs), 'Letters in Uhr pairs can ' \
                                      'only be wired once!'

            # Connects letter pairs to a corresponding aX - bX pair
            for pair, index in zip(pairs, range(1, 11)):
                for letter, socket_id in zip(pair, 'ab'):
                    full_socket_id = str(index) + socket_id
                    socket_data = self._black_red_plug_pairs[full_socket_id]
                    self.pairs[letter] = (full_socket_id, socket_data)

            self._simple_pairs = pairs
        else:
            self._simple_pairs = []
            self._pairs = {}

    @property
    def position(self):
        """Returns current uhr position"""
        return self.relative_board[0]

    @position.setter
    def position(self, position):
        """Sets uhr position"""
        position = int(position)
        while self.position != position % 40:
            self._change_board_offset('relative_board', 1)
            self._change_board_offset('back_board', 1)

    def _compensate(func):
        """Compensates for the rotor rotation"""
        @wraps(func)
        def wrapper(self, absolute_input):
            relative_input = self.relative_board[absolute_input]  # Correct
            relative_output = func(self, relative_input)
            relative_index = self.relative_board.index(relative_output)
            absolute_output = range(40)[relative_index]
            return absolute_output
        return wrapper

    @_compensate
    def _route_forward(self, position):
        """Routes letter from A board to B board, absolute! > does not
        compensate for disc offset"""
        return self.relative_board[self.back_board.index(position)]

    @_compensate
    def _route_backward(self, position):
        """Routes letter from B board to A board, absolute! > does not
        compensate for disc offset"""
        return self.back_board[self.relative_board.index(position)]

    def find_letter(self, board_letter, target):
        """Finds letter based on the target index and target board"""
        for pair in self._pairs.items():
            if board_letter in pair[1][0]:
                if target == pair[1][1][1]:
                    return pair[0]

    def route(self, letter):
        """Routes letter trough the Uhr disk."""
        letter_data = self._pairs[letter.upper()]
        output_pin_index = letter_data[1][0]

        if 'a' in letter_data[0]:
            board = 'a'
        else:
            board = 'b'

        letter = self.find_letter(board, self._route_backward(output_pin_index))

        assert letter, "No letter found!"
        return letter


__all__ = ['EnigmaFactory', 'RotorFactory', 'Enigma1', 'EnigmaM3', 'EnigmaM4',
           'Reflector', 'Stator', 'Rotor', 'UKWD', 'Uhr', 'Luckenfuller']
