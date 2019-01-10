#! /usr/env python3

from v2.newnigma.components import *


class EnigmaAPI:
    """
    Interface object between Qt GUI and Enigma instance, this should be the only source
    of truth for the GUI and its configuration
    """

    def __init__(self, model, reflector, rotors):
        self._data = historical_data[model]
        self._enigma = self._generate_enigma(model, reflector, rotors)
        
    def _generate_enigma(self, model, reflector, rotors):
        return init_enigma(model, reflector, rotors)

    def model(self):
        return self._enigma.model

    def reflector(self):
        return self._enigma.reflector

    def rotors(self):
        return self._enigma.rotors

    def positions(self):
        return self._enigma.positions
