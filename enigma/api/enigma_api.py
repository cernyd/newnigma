#! /usr/env python3

from enigma.core.components import *


class EnigmaAPI:
    """
    Interface object between client and Enigma instance
    """

    def __init__(self, model, reflector, rotors):
        """
        :param model: {str} Enigma machine model label
        :param reflector: {str} Reflector label like "UKW-B"
        :param rotors: {[str, str, str]} Rotor labels
        """
        self._data = historical_data[model]
        self._enigma = self.generate_enigma(model, reflector, rotors)

    # PLUGS
        
    def model(self):  # MODEL PLUG
        return self._enigma.model

    def reflector(self):  # REFLECTOR PLUG
        return self._enigma.reflector

    def rotors(self):  # ROTORS PLUG
        return self._enigma.rotors

    def positions(self, new_positions=None):  # POSITIONS PLUG
        if new_positions is not None:
            self._enigma.positions = new_positions
        else:
            return self._enigma.positions
    
    def ring_settings(self, new_ring_settings=None):
        if new_ring_settings is not None:
            self._enigma.ring_settings = new_ring_settings
        else:
            return self._enigma.ring_settings

    def plug_pairs(self, new_plug_pairs=None):
        if new_plug_pairs is not None:
            self._enigma.plug_pairs = new_plug_pairs
        else:
            return self._enigma.plug_pairs

    def encrypt(self, letter):
        """
        Encrypts letter using the current Enigma object
        :param letter: {char} Letter to encrypt
        """
        return self._enigma.press_key(letter)

    def rotate_rotor(self, rotor_id, by=1, callback=False):
        """
        :param rotor_id: {int} Integer position of the rotor (0 = first rotor, ...)
        :param by: {int} Positive or negative integer describing the number of spaces
        :param callback: {bool} Returns callable wrapped method if True, else only executes, needed to bypass python lambda evaluation problems in for loops
        """
        if callback is True:
            return lambda: self._enigma.rotors[rotor_id].rotate(by)
        else:
            return self._enigma.rotors[rotor_id].rotate(by)

    # Generators

    @classmethod
    def generate_enigma(cls, model, reflector_label, rotor_labels):
        """
        Initializes a complete Enigma instance based on input parameters
        :param model: {str} Enigma model
        :param reflector_label: {str} Reflector label like "UKW-B"
        :param rotor_labels: {[str, str, str]} List of rotor labels like "I", "II", "III"
        """
        rotors = []
        for label in rotor_labels:
            rotors.append(cls.generate_component(model, "Rotor", label))

        reflector = cls.generate_component(model, "Reflector", reflector_label)
        stator = cls.generate_component(model, "Stator")

        return Enigma(model, reflector, rotors, stator)


    @classmethod
    def generate_component(cls, model, comp_type, label=None):
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

    def __str__(self):
        header = "=== %s instance data ===" % self._enigma.model
        footer = "="*len(header)
        message = "\nRotors:              %s\nRotor positions:     %s\nRotor ring settings: %s \nReflector: %s\n"  # \nPlugboard pairs: %s
        rotors = ' '.join([rotor.label for rotor in self._enigma.rotors])
        return header + message % (rotors, ' '.join(self._enigma.positions), ' '.join(map(str, self._enigma.ring_settings)), self._enigma._reflector.label) + footer
