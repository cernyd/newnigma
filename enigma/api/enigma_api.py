#! /usr/env python3

from enigma.core.components import *


class EnigmaAPI:
    """
    Interface object between client and Enigma instance
    """

    def __init__(self, model, reflector, rotors, position_buffer=1000):
        """
        :param model: {str} Enigma machine model label
        :param reflector: {str} Reflector label like "UKW-B"
        :param rotors: {[str, str, str]} Rotor labels
        """
        self._enigma = self.generate_enigma(model, reflector, rotors)

        self.__buffer = []
        self.__buffer_size = position_buffer
        self.__checkpoint = 0

    @property
    def _data(self):
        return historical_data[self.model()]

    # PLUGS

    def rotor_n(self, model=None):
        if model is None:
            return self._enigma.rotor_n()
        else:
            return historical_data[model]['rotor_n']

    def letter_group(self):  # TODO: Used by io textboxes
        return historical_data[self.model()]['letter_group']

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
            self._enigma.reflector(self.generate_component(self.model(), 'Reflector', new_reflector))
        else:
            return self._enigma.reflector()

    def reflector_rotatable(self):
        return self._enigma.reflector_rotatable()

    def rotors(self, new_rotors=None):
        """
        Returns rotors or sets a new one if new_rotors is overriden
        :param new_rotors: {str}
        """
        if new_rotors is not None:
            self._enigma.rotors(self.generate_rotors(self.model(), new_rotors))
        else:
            return self._enigma.rotors()

    def positions(self, new_positions=None):
        """
        Returns positions or sets a new one if new_positions is overriden
        :param new_positions: {str}
        """
        return self._enigma.positions(new_positions)
    
    def ring_settings(self, new_ring_settings=None):
        """
        Returns ring_settings or sets a new one if new_ring_settings is overriden
        :param ring_settings: {str}
        """
        return self._enigma.ring_settings(new_ring_settings)

    def plug_pairs(self, new_plug_pairs=None):
        """
        Returns plug_pairs or sets a new one if new_plug_pairs is overriden
        :param new_plug_pairs: {str}
        """
        return self._enigma.plug_pairs(new_plug_pairs)
    
    def generate_rotate_callback(self, rotor_id, by=1):
        """
        :param rotor_id: {int} Integer position of the rotor
                               (0 = first rotor, ...)
        :param by: {int} Positive or negative integer 
                         describing the number of spaces
        :param callback: {bool} Returns callable wrapped method if True, else 
                                only executes, needed to bypass python 
                                lambda evaluation problems in for loops
        """
        def rotate_rotor(rotor_id, by=1):
            self.__clear_buffer()
            self._enigma.rotate_rotor(rotor_id, by)
            self.set_checkpoint()

        return lambda: rotate_rotor(rotor_id, by)

    def rotate_reflector(self, by=1, callback=False):
        if callback is True:
            return lambda: self._enigma.rotate_reflector(by)
        else:
            self._enigma.rotate_reflector(by)

    def reflector_position(self, new_position=None):
        return self._enigma.reflector_position(new_position)

    def reflector_pairs(self, new_pairs=None):
        return self._enigma.reflector_pairs(new_pairs)

    def uhr(self, x=None):
        return self._enigma.uhr(x)

    # BUFFER TOOLS

    def __serialized_position(self):
        serialized = ''

        for pos in self._enigma.positions():
            if pos in alphabet:
                serialized += "%02d" % alphabet.index(pos)
            else:
                serialized += "%02d" % (int(pos) - 1)

        return int(serialized)

    def set_checkpoint(self):
        self.__checkpoint = self.__serialized_position()

    def __clear_buffer(self):
        self.__buffer = []

    def __save_position(self):
        if len(self.__buffer) == self.__buffer_size:
            print("TODO: BUFFER OVERFLOWING")
            self.__buffer.pop(0)
        self.__buffer.append(self.__serialized_position())


    def revert_by(self, by=1):
        assert by >= 0, "Enigma can only be reverted by 1 or more positions"
        self.__buffer = self.__buffer[:-by]
        
        if not self.__buffer:
            position = self.__checkpoint
        else:
            position = self.__buffer[-1]

        formula = "%0" + str(self.rotor_n()*2) + "d"
        print(position)
        positions = []
        pair = ''
        for letter in formula % position:  # Weird bug that returns instance of EnigmaAPI
            pair += letter
            if len(pair) == 2:
                positions.append(int(pair))
                pair = ''

        self.positions(positions)

    # ENCRYPTION

    def encrypt(self, letter):
        """
        Encrypts letter using the current Enigma object
        :param letter: {char} Letter to encrypt
        """
        output = self._enigma.press_key(letter)
        self.__save_position()
        return output

    # GENERATORS

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
        rotor_n = historical_data[model]['rotor_n']
        plugboard = historical_data[model]['plugboard']
        rotatable_ref = historical_data[model]['rotatable_ref']
        numeric = historical_data[model]['numeric']
            
        return Enigma(model, reflector, rotors, stator, plugboard=plugboard, 
                      rotor_n=rotor_n, rotatable_ref=rotatable_ref, numeric=numeric)

    @classmethod
    def generate_component(cls, model, comp_type, label=None):
        """
        Initializes a Stator, Rotor or Reflector.
        :param model: {str} Enigma machine model
        :param comp_type: {str} "Stator", "Rotor" or "Reflector"
        :param label: {str} or {int} Component label like "I", "II", "UKW-B" or numerical index
                      of their position in historical data (0 = "I", 2 = "II", ...)
        """
        assert model in historical_data, "Invalid enigma model %s!" % model

        data = historical_data[model]
     
        if label is None and comp_type != "Stator":
            raise TypeError("A label has to be supplied for Rotor and Reflector" \
                            "object!")
     
        assert model in historical_data, "The model argument must be in historical" \
                                         "Enigma models!"
     
        component = None
        i = 0
        if comp_type == "Rotor":
            for rotor in data["rotors"]:
                if rotor['label'] == label or label == i:
                    component = Rotor(**rotor)
                    break
                i += 1
            assert component, "No component with label %s found!" % label
        elif comp_type == "Reflector":
            if label == 'UKW-D':
                return UKWD(UKW_D['wiring'])

            for reflector in data["reflectors"]:
                if reflector['label'] == label or label == i:
                    component = Reflector(**reflector, rotatable=data['rotatable_ref'])
                    break
                i += 1
            assert component, "No component with label %s found!" % label
        elif comp_type == "Stator":
            return Stator(**data["stator"])
        else:
            raise TypeError('The comp_type must be "Reflector", "Stator" or "Rotor"')

        return component

    # CONFIG SAVE/LOAD

    def load_from_config(self, config):
        """
        Loads data from dict
        """
        self.model(config['model'])

        self.reflector(config['reflector'])
        pos = config.get('reflector_position', None)
        if pos:
            self._enigma.reflector_position(pos)
        elif self.reflector() == 'UKW-D':
            self.reflector_pairs(config['reflector_wiring'])

        self.rotors(config['rotors'])
        self.positions(config['rotor_positions'])
        self.ring_settings(config['ring_settings'])

        if config.get('uhr_position', None) is not None:
            self._enigma.uhr(True)  # Connect uhr
            self._enigma.uhr_position(config['uhr_position'])

        self.plug_pairs(config['plugs'])
    
    def get_config(self):
        """
        Converts enigma settings to a json serializable dict.
        """
        data = {}
        data['model'] = self._enigma.model()

        data['reflector'] = self._enigma.reflector()
        if self._enigma.reflector_rotatable():
            data['reflector_position'] = self._enigma.reflector_position()
        elif self.reflector() == 'UKW-D':
            data['reflector_wiring'] = self.reflector_pairs()

        data['rotors'] = self._enigma.rotors()
        data['rotor_positions'] = self._enigma.positions()
        data['ring_settings'] = self._enigma.ring_settings()

        if self._enigma.uhr():
            data['uhr_position'] = self._enigma.uhr_position()

        plugs = []
        for plug in self._enigma.plug_pairs():
            plugs.append(''.join(plug))
        data['plugs'] = plugs

        return data

    def __str__(self):
        header = "=== %s instance data ===" % self._enigma.model()

        rotors = "\nRotors: %s" % ' '.join(self._enigma.rotors())

        position = []
        numeric = self._enigma._numeric  # TODO: Refactor
        for pos in self._load_position(self._checkpoint):
            position.append("%02d" % (pos + 1) if numeric else alphabet[pos])
        positions = "\nRotor positions: %s" % ' '.join(position)

        rings = "\nRing settings: %s" % ' '.join(map(str, self._enigma.ring_settings()))


        reflector = "\nReflector: %s" % self._enigma.reflector()
        msg = header + rotors + positions + rings + reflector

        if self.reflector_rotatable():
            msg += "\nReflector position: %s" % self.reflector_position()
        elif self.reflector() == 'UKW-D':
            msg += "\nReflector wiring: %s" % ' '.join(self.reflector_pairs())

        plug_pairs = "\nPlugboard pairs: %s" % ' '.join([''.join(pair) for pair in self._enigma.plug_pairs()])
        msg += plug_pairs

        if self.uhr():
            msg += "\nUhr position: %02d" % self._enigma.uhr_position()

        msg += "\n" + "="*len(header)

        return msg
