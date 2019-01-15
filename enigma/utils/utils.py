from enigma.core.components import *


def init_component(model, comp_type, label=None):
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


def init_enigma(model, rotor_labels, reflector_label):
    rotors = []
    for label in rotor_labels:
        rotors.append(init_component(model, "Rotor", label))

    reflector = init_component(model, "Reflector", reflector_label)
    stator = init_component(model, "Stator")

    return Enigma(model, reflector, rotors, stator)

