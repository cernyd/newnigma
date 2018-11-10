#!/usr/bin/env python3

import pytest
from v2.enigma.components import _RotorBase, historical_data

# "test_cfg": {
#     "default_cfg": {
#         "reflector": "UKW-B",
#         "rotors": [
#             "I",
#             "II",
#             "III"
#         ]
#     },
#     "test_encrypt_decrypt": {
#         "decrypted": "ENIGMAUNITTESTMESSAGE",
#         "encrypted": "FQGAHWLMJAMTJAANUNPDY"
#     },
#     "test_plugboard": {
#         "pairs": [
#             "AQ",
#             "XP",
#             "FG",
#             "DR"
#         ]
#     },
#     "test_positions": {
#         "positions": [
#             "A",
#             "B",
#             "C"
#         ]
#     },
#     "test_reflector": {
#         "reflector": "UKW-B"
#     },
#     "test_ring_settings": {
#         "ring_settings": [
#             "C",
#             "B",
#             "A"
#         ]
#     },
#     "test_rotors": {
#         "rotors": [
#             "III",
#             "I",
#             "II"
#         ]
#     }
# }


@pytest.mark.parametrize('message, result', (
        ("ENIGMAUNITTESTMESSAGE", "FQGAHWLMJAMTJAANUNPDY"),
        ("FQGAHWLMJAMTJAANUNPDY", "ENIGMAUNITTESTMESSAGE")
))
def test_encrypt_decrypt(message, result):
    output = ''
    enigma = None

    for letter in message:
        output += '+'


def test_routing():
    data = historical_data['Enigma1']['rotors'][0]
    base = _RotorBase(data['label'], data['back_board'])
    print("Letter A routed to " + base._route_forward('A'))


# class TestEnigma(unittest.TestCase):
#     """Used to test if enigma class behaves like the real life counterpart"""
#     model = ''
#     cfg_path = []
#
#     def __init__(self, *args, **kwargs):
#         unittest.TestCase.__init__(self, *args, **kwargs)
#         self.cfg = Config(TestEnigma.cfg_path).data['test_cfg']
#         self.subject = None
#         self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.yaml'])
#         self.reset_subject()
#
#     def reset_subject(self):
#         self.subject = self.enigma_factory.produce_enigma('EnigmaM3')
#
#     def test_encrypt_decrypt(self):
#         """Tests if encryption and decryption are working properly"""
#         buffer = self.cfg['test_encrypt_decrypt']
#         for test in permutations(['encrypted', 'decrypted']):
#             self.reset_subject()
#             output = ''
#             for letter in buffer[test[0]]:
#                 output += self.subject.button_press(letter)
#
#             err_msg = 'Failed to {}!'.format(test[1][:-2])
#             self.assertEqual(output, buffer[test[1]], err_msg)
#         with self.assertRaises(AssertionError):
#             self.subject.button_press(18)
#
#     def test_rotors(self):
#         """Tests if rotors are assigned properly"""
#         self.reset_subject()
#         rotors = self.cfg['test_rotors']['rotors']
#         self.subject.rotors = self.enigma_factory.produce_rotor('EnigmaM3',
#                                                                 'rotor', rotors)
#         self.assertEqual(self.subject.rotor_labels, rotors,
#                          'Invalid rotor order assigned!')
#
#     def test_positions(self):
#         """Tests if rotor positions are set properly"""
#         self.reset_subject()
#         positions = self.cfg['test_positions']['positions']
#         self.subject.positions = positions
#         self.assertEqual(self.subject.positions, positions,
#                          'Positions assigned in wrong order!')
#         with self.assertRaises(AssertionError):
#             self.subject.positions = 14651, 'garbage', -15
#
#     def test_reflector(self):
#         """Tests if the reflector is set properly"""
#         self.reset_subject()
#         reflector = self.cfg['test_reflector']['reflector']
#         self.subject.reflector = self.enigma_factory.produce_rotor('EnigmaM3', 'reflector', reflector)
#         self.assertEqual(self.subject.reflector.label, reflector,
#                          'Invalid rotor assigned!')
#         with self.assertRaises(AssertionError):
#             self.subject.reflector = 'garbage_input'
#
#     def test_ring_settings(self):
#         """Tests if ring settings are set properly"""
#         self.reset_subject()
#         ring_settings = self.cfg['test_ring_settings']['ring_settings']
#         self.subject.ring_settings = ring_settings
#         self.assertEqual(self.subject.ring_settings, ring_settings,
#                          'Invalid ring settings assigned!')
#         with self.assertRaises(AssertionError):
#             self.subject.ring_settings = [12, 'garbage_input', 798715]
#
#     def test_plugboard(self):
#         """Checks if plugboard pairs are set propertly"""
#         self.reset_subject()
#         plug_pairs = self.cfg['test_plugboard']['pairs']
#         self.subject.plugboard = {'normal_pairs': plug_pairs}
#
#         err_msg = 'Invalid plugboard pairs assigned!'
#         self.assertEqual(self.subject.plugboard['normal_pairs'], plug_pairs,
#                          err_msg)
#         with self.assertRaises(AttributeError):
#             self.subject.plugboard = 'garbage_input'