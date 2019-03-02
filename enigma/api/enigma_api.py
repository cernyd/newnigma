#! /usr/env python3

from enigma.core.components import (
    UKW_D,
    UKWD,
    Enigma,
    Reflector,
    Rotor,
    Stator,
    alphabet,
    historical,
    format_position,
)


class EnigmaAPI:
    """
    Interface object between client and Enigma instance
    """

    def __init__(self, model, reflector=None, rotors=None, position_buffer=10000):
        """
        :param model: {str} Enigma machine model label
        :param reflector: {str} Reflector label like "UKW-B"
        :param rotors: {[str, str, str]} Rotor labels
        """
        self._enigma = self.generate_enigma(model, reflector, rotors)

        self.__buffer = []
        self.__buffer_size = position_buffer
        self.__checkpoint = 0

    # GETTERS

    def data(self):
        """
        Returns historical data for the current model
        """
        return historical[self.model()]

    def rotor_n(self, model=None):
        """
        Returns rotor count of current model or other model
        :param model: {str} Model to get rotor count for
        """
        if not model:
            return self._enigma.rotor_n()
        return historical[model]["rotor_n"]

    def letter_group(self):
        """
        Returns the historical letter group for this Enigma model
        """
        return historical[self.model()]["letter_group"]

    def model_labels(self, model=None):
        """
        Returns all available labels for rotors and reflectors for the select
        model
        :param model: {str} Enigma model
        """
        model = model if model else self.model()
        labels = lambda component: [item["label"] for item in
                                    historical[model][component]]

        return {
            "reflectors": labels("reflectors"),
            "rotors": labels("rotors")
        }

    def reflector_rotatable(self):
        """
        Returns a value of is not None whether or not the current Enigma model
        supports reflector rotation
        """
        return self._enigma.reflector_rotatable()

    # PLUGS

    def model(self, new_model=None):
        """
        Returns model or sets a new one if new_model is overridden
        :param new_model: {str}
        """
        if new_model is not None:
            labels = self.model_labels(new_model)

            rotors = labels["rotors"][: self.rotor_n(new_model)]
            reflector = labels["reflectors"][0]

            del self._enigma
            self._enigma = self.generate_enigma(new_model, reflector, rotors)
            self.set_checkpoint()
        else:
            return self._enigma.model()

    def reflector(self, new_reflector=None):
        """
        Returns reflector or sets a new one if new_reflector is overridden
        :param new_reflector: {str}
        """
        if new_reflector is not None:
            new_reflector = self.generate_component(
                self.model(), "reflectors", new_reflector
            )
            self._enigma.reflector(new_reflector)
        else:
            return self._enigma.reflector()

    def rotors(self, new_rotors=None):
        """
        Returns rotors or sets a new one if new_rotors is overridden
        :param new_rotors: {str}
        """
        if new_rotors is not None:
            self._enigma.rotors(self.generate_rotors(self.model(), new_rotors))
        else:
            return self._enigma.rotors()

    def positions(self, new_positions=None):
        """
        Returns positions or sets a new one if new_positions is overridden
        :param new_positions: {str}
        """
        return self._enigma.positions(new_positions)

    def ring_settings(self, new_ring_settings=None):
        """
        Returns ring_settings or sets a new one if new_ring_settings
        is overridden
        :param ring_settings: {str}
        """
        return self._enigma.ring_settings(new_ring_settings)

    def plug_pairs(self, new_plug_pairs=None):
        """
        Returns plug_pairs or sets a new one if new_plug_pairs is overridden
        :param new_plug_pairs: {str}
        """
        return self._enigma.plug_pairs(new_plug_pairs)

    def reflector_position(self, new_position=None):
        """
        Returns current reflector position (if any)
        :param new_position: New position to set to the reflector
        """
        return self._enigma.reflector_position(new_position)

    def reflector_pairs(self, new_pairs=None):
        """
        Returns current reflector wiring pairs (if any)
        :param new_pairs: New wiring pair to set to the reflector
        """
        return self._enigma.reflector_pairs(new_pairs)

    def uhr(self, action=None):
        """
        Modifies current Uhr status
        :param action: Will enable Uhr if True, disable if False and return
                       connection status if None
        """
        return self._enigma.uhr(action)

    def uhr_position(self, position=None):
        """  TODO: Add
        """
        return self._enigma.uhr_position(position)

    def generate_rotate_callback(self, rotor_id, by=1):
        """
        Generates a function that will rotate a select rotor by one position
        in the select direction (used by gui)
        :param rotor_id: {int} Integer position of the rotor
                               (0 = first rotor, ...)
        :param by: {int} Positive or negative integer
                         describing the number of spaces
        """

        def rotate_rotor(rotor_id, by=1):
            self.__clear_buffer()
            self._enigma.rotate_rotor(rotor_id, by)
            self.set_checkpoint()

        return lambda: rotate_rotor(rotor_id, by)

    def rotate_reflector(self, by=1, callback=False):
        """
        Rotates reflector by select number of positions, generates a callback
        if specified
        :param by: {int} n positions to rotate (negative number for
                         the opposite direction)
        :param callback: {bool} Will return a lambda that will call
                                this function
        """
        if callback is True:
            return lambda: self._enigma.rotate_reflector(by)
        else:
            self._enigma.rotate_reflector(by)

    # BUFFER TOOLS

    def __serialized_position(self):
        """
        Serializes current rotor positions to a single integer
        For example: [02, 13, 5, 22] -> 2130522
        This method saves space in memory
        """
        serialized = ""

        for pos in self._enigma.positions():
            if pos in alphabet:
                serialized += "%02d" % alphabet.index(pos)
            else:
                serialized += "%02d" % (int(pos) - 1)
        return int(serialized)

    def set_checkpoint(self):
        """
        Sets the starting position of the currently typed message (this can
        later be loaded)
        """
        self.__checkpoint = self.__serialized_position()

    def load_checkpoint(self):
        """
        Sets rotor positions to the checkpoint position
        """
        self.positions(self.checkpoint())

    def checkpoint(self):
        """
        Returns current checkpoint positions
        """
        return self.__load_position(self.__checkpoint)

    def __clear_buffer(self):
        """
        Erases all saved positions in the position buffer
        """
        self.__buffer = []

    def buffer_full(self):
        """Checks if the position buffer has reached its maximum length"""
        return len(self.__buffer) == self.__buffer_size

    def __save_position(self):
        """
        Saves current Enigma rotor position to the position buffer
        """
        if self.buffer_full():
            self.__buffer.pop(0)
        self.__buffer.append(self.__serialized_position())

    def __load_position(self, position):
        """
        Deserializes position from an integer to the original form (list of
        rotor positions)
        :param position: {int} position to be loaded
        """
        formula = "%0" + str(self.rotor_n() * 2) + "d"
        positions = []
        pair = ""
        for letter in formula % position:
            pair += letter
            if len(pair) == 2:
                positions.append(int(pair) + 1)
                pair = ""

        return positions

    def revert_by(self, by=1):
        """
        Reverts by "by" positions back (used when backspace is pressed
        or text is deleted)
        """
        if not by >= 0:
            raise ValueError("Enigma can only be reverted by 1 or more positions")

        self.__buffer = self.__buffer[:-by]

        if not self.__buffer:
            position = self.__checkpoint
        else:
            position = self.__buffer[-1]

        self.positions(self.__load_position(position))

    # ENCRYPTION

    def encrypt(self, text):
        """
        Encrypts text using the current Enigma object, also saves position
        to the position buffer
        :param text: {char} Text to encrypt
        """
        output = ''
        for letter in text:
            output += self._enigma.press_key(letter)
            self.__save_position()
        return output

    # COMPONENT GENERATORS

    @classmethod
    def generate_rotors(cls, model, rotor_labels):
        """
        Generates rotors from supplied labels
        :param rotor_labels: {[str, str, str]}
        """
        rotors = []
        for label in rotor_labels:
            rotors.append(cls.generate_component(model, "rotors", label))
        return rotors

    @classmethod
    def generate_enigma(cls, model, reflector_label=None, rotor_labels=None):
        """
        Initializes a complete Enigma instance based on input parameters
        :param model: {str} Enigma model
        :param reflector_label: {str} Reflector label like "UKW-B"
        :param rotor_labels: {[str, str, str]} List of rotor labels
                                               like "I", "II", "III"
        """
        if not reflector_label:  # TODO: Could use model labels?
            reflector_label = historical[model]["reflectors"][0]["label"]
        reflector = cls.generate_component(model, "reflectors", reflector_label)

        rotor_n = historical[model]["rotor_n"] if reflector_label != "UKW-D" else 3
        if not rotor_labels:  # Default config generation
            rotor_labels = [cfg['label'] for cfg in historical[model]["rotors"][:rotor_n]]
        rotors = cls.generate_rotors(model, rotor_labels)

        plugboard = historical[model]["plugboard"]
        rotatable_ref = historical[model]["rotatable_ref"]
        numeric = historical[model]["numeric"]
        stator = cls.generate_component(model, "stator")

        return Enigma(
            model,
            reflector,
            rotors,
            stator,
            plugboard=plugboard,
            rotor_n=rotor_n,
            rotatable_ref=rotatable_ref,
            numeric=numeric,
        )

    @classmethod
    def generate_component(cls, model, comp_type, label=None):
        """
        Initializes a Stator, Rotor or Reflector.
        :param model: {str} Enigma machine model
        :param comp_type: {str} "stator", "rotors" or "reflectors"
        :param label: {str} or {int} Component label like "I", "II", "UKW-B" or
                                     numerical index of their position in
                                     historical data (0 = "I", 2 = "II", ...)
        """
        try:
            data = historical[model]
        except KeyError:
            raise ValueError("Invalid enigma model %s!" % model)

        final_data = None
        if comp_type == "stator":
            return Stator(**data[comp_type])
        if type(label) == int:
            final_data = data[comp_type][label]
        else:
            for comp_data in data[comp_type]:
                if comp_data["label"] == label:
                    final_data = comp_data
                    break

        if not final_data:
            raise ValueError("No %s with label %s found!" % (comp_type, label))

        if comp_type == "rotors":
            return Rotor(**final_data)
        elif comp_type == "reflectors":
            if label == "UKW-D":
                return UKWD(UKW_D["wiring"])
            return Reflector(**final_data, rotatable=data["rotatable_ref"])

    # CONFIG SAVE/LOAD

    def load_from_config(self, config):
        """
        Generates components and sets their settings based on input data
        :param config: {dict} Dictionary of saved settings
        """
        old_config = self.get_config()

        try:
            self.model(config["model"])
            self.reflector(config["reflector"])
            self.rotors(config["rotors"])
            self.positions(config["rotor_positions"])
            self.ring_settings(config["ring_settings"])

            try:
                self._enigma.reflector_position(config.get("reflector_position", None))
            except (KeyError, ValueError):
                pass

            try:
                self.reflector_pairs(config["reflector_wiring"])
            except (KeyError, ValueError):
                pass

            if "uhr_position" in config:
                self._enigma.uhr('connect')
                self.uhr_position(config["uhr_position"])

            self.plug_pairs(config["plug_pairs"])
        except Exception as e:
            self.load_from_config(old_config)
            raise

    def get_config(self):
        """
        Converts enigma settings to a json serializable dict (but can be used
        for any purpose)
        """
        data = {}
        data["model"] = self._enigma.model()
        data["reflector"] = self._enigma.reflector()
        data["rotors"] = self._enigma.rotors()
        data["rotor_positions"] = self._enigma.positions()
        data["ring_settings"] = self._enigma.ring_settings()
        data["plug_pairs"] = []
        for plug in self._enigma.plug_pairs():
            data["plug_pairs"].append("".join(plug))

        try:
            data["reflector_position"] = self._enigma.reflector_position()
        except ValueError:
            pass
        try:
            data["reflector_wiring"] = self.reflector_pairs()
        except ValueError:
            pass
        try:
            data["uhr_position"] = self.uhr_position()
        except ValueError:
            pass

        return data

    # STRING REPRESENTATION OF API DATA

    def __str__(self):
        data = self.get_config()
        header = "Enigma model: %s" % data["model"]
        rotors = "\nRotors: %s" % " ".join(data["rotors"])
        pos = []
        for i in self.checkpoint():
            pos.append(format_position(i, self._enigma._numeric))

        positions = "\nRotor positions: %s" % " ".join(pos)
        rings = "\nRing settings: %s" % " ".join(map(str, data["ring_settings"]))
        reflector = "\nReflector: %s" % data["reflector"]
        msg = header + rotors + positions + rings + reflector

        try:
            msg += "\nReflector position: %s" % data["reflector_position"]
        except KeyError:
            pass

        try:
            msg += "\nReflector wiring: %s" % " ".join(data["reflector_wiring"])
        except KeyError:
            pass

        plug_pairs = "\nPlugboard pairs: %s" % " ".join(data["plug_pairs"])
        msg += plug_pairs

        if self.uhr():
            msg += "\nUhr position: %02d" % data["uhr_position"]

        msg += "\n" + "=" * 40

        return msg
