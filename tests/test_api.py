#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice, choices, randint, sample, shuffle
from string import ascii_uppercase as alphabet

import pytest

from enigma.api.enigma_api import EnigmaAPI
from enigma.core.components import Rotor, historical

trash_data = ("iweahbrnawjhb", EnigmaAPI, 12341123, -1332, "heaaafs", "", Rotor,
              "Engima", ["fweafawe", "4324", 43, None], "č", "čěšč", ("š", "+", "6"))


def generate_pairs(k):
    pairs = []
    available = list(alphabet)
    while available:
        shuffle(available)
        pairs.append(available.pop() + available.pop())

    return list(sample(pairs, k=k))


@pytest.mark.parametrize("settings, rotor_n", (
    (("Enigma M3", "UKW-B", ["I", "II", "III"]), 3),
    (("Enigma I", "UKW-A", ["I", "II", "V"]), 3),
    (("Enigma M4", "UKW-b", ["I", "II", "V", "VI"]), 4),
    (("Enigma M4", "UKW-D", ["I", "II", "V"]), 3),
))
def test_rotor_n(settings, rotor_n):
    enigma_api = EnigmaAPI(*settings)
    assert enigma_api.rotor_n() == rotor_n, "Incorrect rotor_n value!"

def test_data():
    enigma_api = EnigmaAPI("Enigma M3", "UKW-B", ["I", "II", "III"])
    assert enigma_api.data() == historical["Enigma M3"]
    enigma_api.model("Enigma M4")
    assert enigma_api.data() == historical["Enigma M4"]


@pytest.mark.parametrize("model, letter_group", (
    ("Enigma M4", 4),
    ("Enigma M3", 5),
    ("Norenigma", 5),
    ("Enigma K", 5),
))
def test_letter_group(model, letter_group):
    enigma_api = EnigmaAPI(model)
    assert enigma_api.letter_group() == letter_group, "Incorrect letter group length!"


@pytest.mark.parametrize("model, labels", (
    ("Enigma M4", {"rotors": ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "Beta", "Gamma"],
                  "reflectors": ["UKW-b", "UKW-c", "UKW-D"]}),
    ("Enigma I", {"rotors": ["I", "II", "III", "IV", "V"],
                 "reflectors": ["UKW-A", "UKW-B", "UKW-C", "UKW-D"]})
))
def test_model_labels(model, labels):
    enigma_api = EnigmaAPI(model)
    assert enigma_api.model_labels(model) == labels, "Incorrect (or incomplete) list of labels for selected model!"


def test_reflector_rotatable():
    for model, data in historical.items():
        assert EnigmaAPI(model).reflector_rotatable() == data['rotatable_ref']


def test_model_set():
    enigma_api = EnigmaAPI("Enigma I")
    labels = list(historical.keys())

    for _ in range(100):
        new_model = choice(labels)
        enigma_api.model(new_model)
        assert enigma_api.model() == new_model

    for trash in trash_data:
        with pytest.raises(ValueError):
            enigma_api.model(trash)


def test_reflector_set():
    enigma_api = EnigmaAPI("Enigma I")
    for new_reflector in "UKW-B", "UKW-A", "UKW-D":
        enigma_api.reflector(new_reflector)
        assert enigma_api.reflector() == new_reflector

    for trash in trash_data:
        with pytest.raises(ValueError):
            enigma_api.reflector(trash)


def test_rotors_set():
    enigma_api = EnigmaAPI("Enigma I")
    rotors = ["I", "II", "III", "IV", "V"]

    for _ in range(100):
        new_rotors = choices(rotors, k=3)
        enigma_api.rotors(new_rotors)
        assert enigma_api.rotors() == new_rotors

    for _ in range(100):
        new_rotors = choices(range(len(rotors)), k=3)
        enigma_api.rotors(new_rotors)
        assert enigma_api.rotors() == [rotors[i] for i in new_rotors]

    for trash in trash_data:
        with pytest.raises(ValueError):
            enigma_api.rotors(trash)


def test_positions_set():
    enigma_api = EnigmaAPI("Enigma M4")
    for _ in range(100):
        new_positions = [randint(-30, 30) for _ in range(4)]

        if not all(map(lambda x: x in range(1, 27), new_positions)):
            with pytest.raises(ValueError):
                enigma_api.positions(new_positions)
        else:
            enigma_api.positions(new_positions)
            assert enigma_api.positions() == tuple(map(lambda x: alphabet[x-1], new_positions))


def test_ring_settings_set():
    enigma_api = EnigmaAPI("Enigma M4")
    for _ in range(100):
        new_ring_settings = [randint(-30, 30) for _ in range(4)]

        if not all(map(lambda x: x in range(1, 27), new_ring_settings)):
            with pytest.raises(ValueError):
                enigma_api.ring_settings(new_ring_settings)
        else:
            enigma_api.ring_settings(new_ring_settings)
            assert enigma_api.ring_settings() == new_ring_settings


def test_plug_pairs():
    pairs = generate_pairs(randint(0, 13))
    enigma_api = EnigmaAPI("Enigma M3")
    enigma_api.plug_pairs(pairs)
    assert enigma_api.plug_pairs() == pairs


def test_reflector_position():
    enigma_api = EnigmaAPI("Enigma K", "UKW")

    for _ in range(100):
        new_position = randint(-30, 30)
        if new_position not in range(1, 27):
            with pytest.raises(ValueError):
                enigma_api.reflector_position(new_position)
        else:
            enigma_api.reflector_position(new_position)
            assert enigma_api.reflector_position() == alphabet[new_position - 1]


@pytest.mark.parametrize("pairs, should_fail", (
    (["AB", "CD", "EF", "GH", "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ"], False),
    (["AB", "CD", "EF", "GH", "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ", "JY"], True),
    (["", "CD", "EF", "GH", "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ", "JY"], True),
    (["A", "CD", "EF", "GH", "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ", "JY"], True),
    (["EF", "GH", "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ"], True),
    ([132, "CD", "EF", EnigmaAPI, "IK", "LM", "NO", "PQ", "RS", "TU", "VW", "XZ"], True),
    ([1], True),
        
))
def test_reflector_pairs(pairs, should_fail):
    enigma_api = EnigmaAPI("Enigma M4")
    enigma_api.reflector("UKW-D")
    if should_fail:
        with pytest.raises(ValueError):
            enigma_api.reflector_pairs(pairs)
    else:
        enigma_api.reflector_pairs(pairs)
        assert type(enigma_api.encrypt("ABCD"))


def test_uhr():
    enigma_api = EnigmaAPI("Enigma M3")
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


def test_generate_rotor_callback():
    enigma_api = EnigmaAPI("Enigma I")

    for i in list(range(3))*10:
        by = randint(0, 25)
        callback = enigma_api.generate_rotate_callback(i, by)
        callback()
        assert int(enigma_api.positions()[i]) - 1 == by
        enigma_api.positions([1, 1, 1])
