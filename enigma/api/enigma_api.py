#! /usr/env python3

from enigma.core.components import *
from math import factorial


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
        self._enigma = self.generate_enigma(model, reflector, rotors)

    def total_permutations(self, with_reflectors=False):
        """
        Returns total possible permutations for all rotors
        """
        total_rotors = len(self._data['rotors'])
        rotor_combinations = int(factorial(total_rotors)/factorial(total_rotors-self.rotor_n()))
        total_reflectors = len(self._data['reflectors'])
        reflector_combinations = int(factorial(total_reflectors)/factorial(total_reflectors-1))
        rotor_settings = 26**self.rotor_n()
        total_plugboard = int(factorial(26)/(factorial(26-20)*(2**10)*factorial(10)))  # CORRECT
        
        result = rotor_combinations*rotor_settings*total_plugboard
        if with_reflectors:
            return result*reflector_combinations
        else:
            return result

    @property
    def _data(self):
        return historical_data[self.model()]

    # PLUGS

    def rotor_n(self, model=None):
        if model is None:
            return self._data['rotor_n']
        else:
            return historical_data[model]['rotor_n']

    def letter_group(self):
        return self._data['letter_group']

    def model_labels(self, model=None):
        """
        Returns all available labels for rotors and reflectors for the select
        model
        :param model: {str} Enigma model
        """
        if model is None:
            model = self.model()

        refs = [reflector['label'] for reflector in historical_data[model]['reflectors']]
        rotors = [rotor['label'] for rotor in historical_data[model]['rotors']]

        return {'reflectors': refs, 'rotors': rotors}

    def model(self, new_model=None):
        """
        Returns model or sets a new one if new_model is overriden
        :param new_model: {str}
        """
        if new_model is not None:
            labels = self.model_labels(new_model)

            rotors = labels['rotors'][:historical_data[new_model]['rotor_n']]
            reflector = labels['reflectors'][0]

            del self._enigma
            self._enigma = self.generate_enigma(new_model, reflector, rotors)
        else:
            return self._enigma.model()

    def reflector(self, new_reflector=None):
        """
        Returns reflector or sets a new one if new_reflector is overriden
        :param new_reflector: {str}
        """
        if new_reflector is not None:
            self._enigma._reflector = self.generate_component(self.model(), 'Reflector', new_reflector)
        else:
            return self._enigma._reflector

    def rotors(self, new_rotors=None):
        """
        Returns rotors or sets a new one if new_rotors is overriden
        :param new_rotors: {str}
        """
        if new_rotors is not None:
            self._enigma.rotors = self.generate_rotors(self.model(), new_rotors)
        else:
            return self._enigma.rotors()

    def positions(self, new_positions=None):
        """
        Returns positions or sets a new one if new_positions is overriden
        :param new_positions: {str}
        """
        self._enigma.positions(new_positions)
    
    def ring_settings(self, new_ring_settings=None):
        """
        Returns ring_settings or sets a new one if new_ring_settings is overriden
        :param ring_settings: {str}
        """
        self._enigma.ring_settings(new_ring_settings)

    def plug_pairs(self, new_plug_pairs=None):
        """
        Returns plug_pairs or sets a new one if new_plug_pairs is overriden
        :param new_plug_pairs: {str}
        """
        self._enigma.plug_pairs(new_plug_pairs)

    def encrypt(self, letter):
        """
        Encrypts letter using the current Enigma object
        :param letter: {char} Letter to encrypt
        """
        return self._enigma.press_key(letter)

    def rotate_rotor(self, rotor_id, by=1, callback=False):
        """
        :param rotor_id: {int} Integer position of the rotor
                               (0 = first rotor, ...)
        :param by: {int} Positive or negative integer 
                         describing the number of spaces
        :param callback: {bool} Returns callable wrapped method if True, else 
                                only executes, needed to bypass python 
                                lambda evaluation problems in for loops
        """
        if callback is True:
            return lambda: self._enigma.rotate_rotor(rotor_id, by)
        else:
            return self._enigma.rotate_rotor(rotor_id, by)

    # Generators

    @classmethod
    def generate_rotors(cls, model, rotor_labels):
        """
        Generates rotors from supplied labels
        :param rotor_labels: {[str, str, str]}
        """
        rotors = []
        for label in rotor_labels:
            rotors.append(cls.generate_component(model, "Rotor", label))
        return rotors

    @classmethod
    def generate_enigma(cls, model, reflector_label=None, rotor_labels=None):
        """
        Initializes a complete Enigma instance based on input parameters
        :param model: {str} Enigma model
        :param reflector_label: {str} Reflector label like "UKW-B"
        :param rotor_labels: {[str, str, str]} List of rotor labels like "I", "II", "III"
        """
        rotors = cls.generate_rotors(model, rotor_labels)
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

    def load_from_config(self, config):
        """
        Loads data from dict
        """
        self.model(config['model'])
        self.reflector(config['reflector'])
        self.rotors(config['rotors'])
        self.positions(config['rotor_positions'])
        self.plug_pairs(config['plugs'])
        self.ring_settings(config['ring_settings'])
        self._enigma.uhr_position(config['uhr_position'])
    
    def get_config(self):
        """
        Converts enigma settings to a json serializable dict.
        """
        data = {}
        data['model'] = self._enigma.model
        data['rotors'] = [rotor.label for rotor in self._enigma.rotors]
        data['rotor_positions'] = self._enigma.positions
        data['ring_settings'] = self._enigma.ring_settings
        data['reflector'] = self._enigma._reflector.label
        data['uhr_position'] = self._enigma.uhr_position()
        data['uhr_connected'] = self._enigma.uhr_connected()

        plugs = []
        for plug in self._enigma.plug_pairs:
            plugs.append(''.join(plug))
        data['plugs'] = plugs

        return data

    def __str__(self):
        header = "=== %s instance data ===" % self._enigma.model
        footer = "="*len(header)
        message = "\nRotors:              %s\nRotor positions:     %s\nRotor ring settings: %s \nReflector: %s\n"  # \nPlugboard pairs: %s
        rotors = ' '.join([rotor.label for rotor in self._enigma.rotors])
        return header + message % (rotors, ' '.join(self._enigma.positions), ' '.join(map(str, self._enigma.ring_settings)), self._enigma._reflector.label) + footer
