#!/usr/bin/env python3

import pytest
from v2.enigma.components import Rotor, historical_data, Reflector, Enigma, Stator, init_component
from string import ascii_uppercase as alphabet


@pytest.mark.parametrize('message, result', (
        ("ENIGMAUNITTESTMESSAGE", "FQGAHWLMJAMTJAANUNPDY"),
        ("FQGAHWLMJAMTJAANUNPDY", "ENIGMAUNITTESTMESSAGE")
))
def test_encrypt_decrypt(message, result):
    output = ''
    enigma = None

    for letter in message:
        output += '+'


def test_single_encrypt():
    base = init_component('Enigma1', 'Rotor', 'I')

    assert base.forward('A') == 'E'
    base.rotate()
    assert base.forward('A') == 'L'
    base.rotate()
    assert base.forward('A') == 'O'

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
    data = historical_data['EnigmaM3']
    reflector = init_component('EnigmaM3', 'Reflector', 'UKW-B')
    stator = init_component('EnigmaM3', 'Stator')
    rotors = []

    for i in 0, 1, 2:
        print(data['rotors'][i])
        rotors.append(Rotor(**data['rotors'][i]))
    enigma = Enigma(reflector, rotors, stator)

    for letter in 'BDZGOW':
        assert enigma.press_key('A') == letter

