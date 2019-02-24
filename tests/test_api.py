#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enigma.api.enigma_api import EnigmaAPI
from enigma.core.components import *
import pytest
from random import choice, choices, randint, shuffle, sample
from string import ascii_uppercase as alphabet

trash_data = ("iweahbrnawjhb", EnigmaAPI, 12341123, None, -1332, "heaaafs", "",
              "Engima", ["fweafawe", "4324", 43, None], "č", "čěšč", ("š", "+", "6"))


def generate_pairs(k):
    pairs = []
    available = list(alphabet)
    while available:
        shuffle(available)
        pairs.append(available.pop() + available.pop())

    return list(sample(pairs, k=k))


@pytest.mark.parametrize("settings, rotor_n", (
    (("EnigmaM3", "UKW-B", ["I", "II", "III"]), 3),
    (("Enigma1", "UKW-A", ["I", "II", "V"]), 3),
    (("EnigmaM4", "UKW-b", ["I", "II", "V", "VI"]), 4),
    (("EnigmaM4", "UKW-D", ["I", "II", "V"]), 3),
))
def test_rotor_n(settings, rotor_n):
    enigma_api = EnigmaAPI(*settings)
    assert enigma_api.rotor_n() == rotor_n, "Incorrect rotor_n value!"

def test_data():
    enigma_api = EnigmaAPI("EnigmaM3", "UKW-B", ["I", "II", "III"])
    assert enigma_api.data() == historical["EnigmaM3"]
    enigma_api.model("EnigmaM4")
    assert enigma_api.data() == historical["EnigmaM4"]


@pytest.mark.parametrize("model, letter_group", (
    ("EnigmaM4", 4),
    ("EnigmaM3", 5),
    ("Norenigma", 5),
    ("EnigmaK", 5),
))
def test_letter_group(model, letter_group):
    enigma_api = EnigmaAPI(model)
    assert enigma_api.letter_group() == letter_group, "Incorrect letter group length!"


@pytest.mark.parametrize("model, labels", (
    ("EnigmaM4", {"rotors": ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "Beta", "Gamma"),
                  "reflectors": ("UKW-b", "UKW-c", "UKW-D")}),
    ("Enigma1", {"rotors": ("I", "II", "III", "IV", "V"),
                 "reflectors": ("UKW-A", "UKW-B", "UKW-C", "UKW-D")})
))
def test_model_labels(model, labels):
    enigma_api = EnigmaAPI(model)
    assert enigma_api.model_labels() == labels, "Incorrect (or incomplete) list of labels for selected model!"


def test_reflector_rotatable():
    for model, data in historical.items():
        assert EnigmaAPI(model).reflector_rotatable() == data['rotatable_ref']


def test_model_set():
    enigma_api = EnigmaAPI("Enigma1")
    labels = list(historical.keys())
    for _ in range(100):
        new_model = choice(labels)
        enigma_api.model(new_model)
        assert enigma_api.model() == new_model

    return  # TODO: Sanitize
    for trash in trash_data:
        enigma_api.model(trash)


def test_reflector_set():
    enigma_api = EnigmaAPI("Enigma1")
    for new_reflector in "UKW-B", "UKW-A", "UKW-D":
        enigma_api.reflector(new_reflector)
        assert enigma_api.reflector() == new_reflector

    return  # TODO: Sanitize
    for trash in trash_data:
        with pytest.raises(ValueError):
            enigma_api.reflector(trash)


def test_rotors_set():
    enigma_api = EnigmaAPI("Enigma1")
    rotors = ["I", "II", "III", "IV", "V"]

    for _ in range(100):
        new_rotors = choices(rotors, k=3)
        enigma_api.rotors(new_rotors)
        assert enigma_api.rotors() == new_rotors

    for _ in range(100):
        new_rotors = choices(range(len(rotors)), k=3)
        enigma_api.rotors(new_rotors)
        assert enigma_api.rotors() == [rotors[i] for i in new_rotors]

    return  # TODO: Sanitize
    for trash in trash_data:
        with pytest.raises(ValueError):
            enigma_api.rotors(trash)


def test_positions_set():
    return
    enigma_api = EnigmaAPI("EnigmaM4")
    for _ in range(100):
        new_positions = [randint(1, 26) for _ in range(4)]
        enigma_api.positions(new_positions)
        assert enigma_api.positions() == new_positions


def test_ring_settings_set():
    enigma_api = EnigmaAPI("EnigmaM4")
    for _ in range(100):
        new_ring_settings = [randint(1, 26) for _ in range(4)]
        enigma_api.ring_settings(new_ring_settings)
        assert enigma_api.ring_settings() == new_ring_settings


def test_plug_pairs():  # TODO: Finish
    pairs = generate_pairs(randint(0, 13))
    enigma_api = EnigmaAPI("EnigmaM3")
    enigma_api.plug_pairs(pairs)
    assert enigma_api.plug_pairs() == pairs


def test_reflector_position():  # TODO: Finish
    pass


def test_reflector_pairs():  # TODO: Finish
    pass


def test_uhr():  # TODO: Finish
    enigma_api = EnigmaAPI("EnigmaM3")
    pairs = generate_pairs(10)
    enigma_api.uhr('connect')
    enigma_api.plug_pairs(pairs)
    correct, other = sample(range(0, 40), 2)
    enigma_api.uhr_position(correct)

    message = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    enigma_api.set_checkpoint()
    encrypted = enigma_api.encrypt(message)
    enigma_api.load_checkpoint()
    assert enigma_api.encrypt(encrypted) == message
    enigma_api.uhr_position(other)
    assert enigma_api.encrypt(encrypted) != message

    # Test Uhr position 00 compatibility mode
    enigma_api.load_checkpoint()
    enigma_api.uhr_position(0)
    with_uhr = enigma_api.encrypt(message)

    enigma_api.load_checkpoint()
    enigma_api.uhr('disconnect')
    enigma_api.plug_pairs(pairs)
    without_uhr = enigma_api.encrypt(message)

    assert with_uhr == without_uhr


def test_generate_rotor_callback():  # TODO: Finish
    pass


def test_rotate():  # TODO: Finish
    pass


def test_buffer():  # TODO: Finish
    pass


def test_encrypt():
    pass


def test_generate():
    pass


def test_config_save_load():
    pass


def test_str():
    pass