#!/usr/bin/env python3

import pytest
from v2.enigma.components import Enigma, Plugboard, init_component, init_enigma
from string import ascii_uppercase as alphabet


def test_single_encrypt():
    base = init_component('Enigma1', 'Rotor', 'I')

    assert base.forward('A') == 'E'
    base.rotate()
    assert base.forward('A') == 'J'
    base.rotate()
    assert base.forward('A') == 'K'

    # "Looping back" to position 0 should produce the same result as in default position
    base.rotate(24)
    assert base.forward('A') == 'E'


def test_routing():
    """
    Tests if the forward routing is being routed correctly in the opposite direction (taking the
    relative rotor position into account)
    """
    base = init_component('Enigma1', 'Rotor', 'I')

    for i in 1, 3, -2, 5, 7, 20:
        for letter in alphabet:
            assert letter == base.backward(base.forward(letter)), \
                "Backwards routing doesn't return to the original location!"
            base.rotate(i)


@pytest.mark.parametrize('offset_by, result', (
    (5, 5), (-1, 25), (26, 0), (15, 15), (50, 24), (-40, 12), (25, 25)
))
def test_rotation(offset_by, result):
    base = init_component('Enigma1', 'Rotor', 'I')
    base.rotate(offset_by=offset_by)
    assert base.offset == result, "Rotor offset is not being calculated correctly"


def test_position():
    base = init_component('Enigma1', 'Rotor', 'I')

    base.rotate()
    assert base.position(True) == "02"
    assert base.position() == "B"
    base.rotate(20)
    assert base.position() == "V"


def test_reflector():
    reflector = init_component('EnigmaM3', 'Reflector', 'UKW-B')

    result = reflector.reflect('A')
    assert 'A' == reflector.reflect(result)


def test_turnover():
    base = init_component('EnigmaM4', 'Rotor', 'VI')

    for _ in range(50):
        if base.in_turnover:
            assert base.position() in base.turnover
        base.rotate()


def test_enigma():
    enigma = init_enigma('EnigmaM3', ["I", "II", "III"], "UKW-B")

    result = ''
    for _ in 'BDZGOW':
        result += enigma.press_key('A')

    assert result == 'BDZGOW'


    enigma = init_enigma('EnigmaM4', ["I", "II", "III", "IV"], "UKW-B")


@pytest.mark.parametrize('model, n_rotors, should_fail', (
    ("EnigmaM4", 4, False),
    ("EnigmaM3", 3, False),
    ("EnigmaM3", 7, True),
    ("EnigmaMX", 3, True),
    ("EnigmaM3", 3, False),
    (33213, 3, True)
))
def test_enigma_models(model, n_rotors, should_fail):
    rotors = range(n_rotors)
    # Fake values instead of rotors because they are not needed in this test

    if should_fail:
        with pytest.raises(AssertionError):
            Enigma(model, "UKW-B", rotors, None)
    else:
        Enigma(model, "UKW-B", rotors, None)


@pytest.mark.parametrize('model, n_rotors, should_fail', (
    ("EnigmaMF", 4, True),
    ("EnigmaM", 4, True),
    ("Enigma", 4, True),
    ("EnigmaM4", 4, False),
    ("EnigmaK", 3, False),
))
def test_init_enigma(model, n_rotors, should_fail):
    rotors = range(n_rotors)
    # Fake values instead of rotors because they are not needed in this test

    if should_fail:
        with pytest.raises(KeyError):
            init_enigma(model, rotors, "UKW-B")
    else:
        init_enigma(model, rotors, "UKW-B")


def test_plugboard():
    plugboard = Plugboard(['AB', 'CD', 'YZ'])

    assert plugboard.route('A') == 'B'
    assert plugboard.route('B') == 'A'
    assert plugboard.route('C') == 'D'
    assert plugboard.route('D') == 'C'
    assert plugboard.route('Y') == 'Z'
    assert plugboard.route('Z') == 'Y'
    assert plugboard.route('G') == 'G'
    assert plugboard.route('I') == 'I'
