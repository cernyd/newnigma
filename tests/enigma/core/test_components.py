#!/usr/bin/env python3

import pytest
from enigma.core.components import Enigma, Plugboard
from enigma.api.enigma_api import EnigmaAPI
from string import ascii_uppercase as alphabet


def test_single_encrypt():
    base = EnigmaAPI.generate_component('Enigma1', 'Rotor', 'I')

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
    base = EnigmaAPI.generate_component('Enigma1', 'Rotor', 'I')

    for i in 1, 3, -2, 5, 7, 20:
        for letter in alphabet:
            assert letter == base.backward(base.forward(letter)), \
                "Backwards routing doesn't return to the original location!"
            base.rotate(i)

def test_implementation():
    """
    Tests the implementation by encrypting each letter of the alphabet
    4000 times and checking if the encrypted message does not contain the 
    letter (this must always be true because the Enigma worked this way)

    The number of iterations is arbitrary (not to slow down the testing process)
    """
    enigma = EnigmaAPI.generate_enigma('EnigmaM3', "UKW-B", ["I", "II", "III"])

    for letter in alphabet:
        for _ in range(4000):
            assert enigma.press_key(letter) != letter, "Enigma implementation wrong!"

@pytest.mark.parametrize('offset_by, result', (
    (5, 5), (-1, 25), (26, 0), (15, 15), (50, 24), (-40, 12), (25, 25)
))
def test_rotation(offset_by, result):
    base = EnigmaAPI.generate_component('Enigma1', 'Rotor', 'I')
    base.rotate(offset_by=offset_by)
    assert base.offset == result, "Rotor offset is not being calculated correctly"


def test_position():
    base = EnigmaAPI.generate_component('Enigma1', 'Rotor', 'I')

    base.rotate()
    assert base.position(True) == "02"
    assert base.position() == "B"
    base.rotate(20)
    assert base.position() == "V"


def test_reflector():
    reflector = EnigmaAPI.generate_component('EnigmaM3', 'Reflector', 'UKW-B')

    result = reflector.reflect('A')
    assert 'A' == reflector.reflect(result)


def test_turnover():
    base = EnigmaAPI.generate_component('EnigmaM4', 'Rotor', 'VI')

    for _ in range(50):
        if base.in_turnover:
            assert base.position() in base.turnover
        base.rotate()


def test_enigma():
    enigma = EnigmaAPI.generate_enigma('EnigmaM3', "UKW-B", ["I", "II", "III"])

    result = ''
    for _ in 'BDZGOW':
        result += enigma.press_key('A')

    assert result == 'BDZGOW'


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
def test_generate_enigma(model, n_rotors, should_fail):
    rotors = range(n_rotors)
    # Fake values instead of rotors because they are not needed in this test

    if should_fail:
        with pytest.raises(KeyError):
            EnigmaAPI.generate_enigma(model, "UKW-B", rotors)
    else:
        EnigmaAPI.generate_enigma(model, "UKW-B", rotors)


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


@pytest.mark.parametrize('model, rotors, reflector, positions, ring_settings, plug_pairs, message, correct_result', (
    (  # Enigma instruction manual message
        'Enigma1', ('II', 'I', 'III'), 'UKW-A', "ABL", (23, 12, 21), ("AM", "FI", "NV", "PS", "TU", "WZ"),
        "GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ",
        "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT"
    ),
    (  # Operation Barbarossa message 1
        'EnigmaM3', ('II', 'IV', 'V'), 'UKW-B', "BLA", (1, 20, 11),  ("AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"),
        "EDPUDNRGYSZRCXNUYTPOMRMBOFKTBZREZKMLXLVEFGUEYSIOZVEQMIKUBPMMYLKLTTDEISMDICAGYKUACTCDOMOHWXMUUIAUBSTSLRNBZSZWNRFXWFYSSXJZVIJHIDISHPRKLKAYUPADTXQSPINQMATLPIFSVKDASCTACDPBOPVHJK",
        "AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX"
    ),
    (  # Operation Barbarossa message 2
        'EnigmaM3', ('II', 'IV', 'V'), 'UKW-B', "LSD", (1, 20, 11),  ("AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"),
        "SFBWDNJUSEGQOBHKRTAREEZMWKPPRBXOHDROEQGBBGTQVPGVKBVVGBIMHUSZYDAJQIROAXSSSNREHYGGRPISEZBOVMQIEMMZCYSGQDGRERVBILEKXYQIRGIRQNRDNVRXCYYTNJR",
        "DREIGEHTLANGSAMABERSIQERVORWAERTSXEINSSIEBENNULLSEQSXUHRXROEMXEINSXINFRGTXDREIXAUFFLIEGERSTRASZEMITANFANGXEINSSEQSXKMXKMXOSTWXKAMENECXK"
    ),
    (  # Schranhorst
        'EnigmaM3', ('III', 'VI', 'VIII'), 'UKW-B', "UZV", (0, 7, 12), ("AN", "EZ", "HK", "IJ", "LR", "MQ", "OT", "PV", "SW", "UX"),
        "YKAENZAPMSCHZBFOCUVMRMDPYCOFHADZIZMEFXTHFLOLPZLFGGBOTGOXGRETDWTJIQHLMXVJWKZUASTR",
        "STEUEREJTANAFJORDJANSTANDORTQUAAACCCVIERNEUNNEUNZWOFAHRTZWONULSMXXSCHARNHORSTHCO"
    ),
    (  # U-264
        'EnigmaM4', ('Beta', 'II', 'IV', 'I'), 'UKW-b', "VJNA", (0, 0, 0, 21), ("AT", "BL", "DF", "GJ", "HM", "NW", "OP", "QY", "RZ", "VX"),
        "NCZWVUSXPNYMINHZXMQXSFWXWLKJAHSHNMCOCCAKUQPMKCSMHKSEINJUSBLKIOSXCKUBHMLLXCSJUSRRDVKOHULXWCCBGVLIYXEOAHXRHKKFVDREWEZLXOBAFGYUJQUKGRTVUKAMEURBVEKSUHHVOYHABCJWMAKLFKLMYFVNRIZRVVRTKOFDANJMOLBGFFLEOPRGTFLVRHOWOPBEKVWMUQFMPWPARMFHAGKXIIBG",
        "VONVONJLOOKSJHFFTTTEINSEINSDREIZWOYYQNNSNEUNINHALTXXBEIANGRIFFUNTERWASSERGEDRUECKTYWABOSXLETZTERGEGNERSTANDNULACHTDREINULUHRMARQUANTONJOTANEUNACHTSEYHSDREIYZWOZWONULGRADYACHTSMYSTOSSENACHXEKNSVIERMBFAELLTYNNNNNNOOOVIERYSICHTEINSNULL"
    )
))
def test_historical_messages(model, rotors, reflector, positions, ring_settings, plug_pairs, message, correct_result):
    # Enigma instruction manual message
    enigma = EnigmaAPI.generate_enigma(model, reflector, rotors)
    enigma.positions = positions
    enigma.ring_settings = ring_settings
    enigma.plug_pairs = plug_pairs

    result = ''
    for letter in message:
        result += enigma.press_key(letter)

    assert result == correct_result


def test_cli():
    import subprocess

    command = "./enigma.py --cli --model Enigma1 --rotors II I III --reflector UKW-A --positions A B L --ring_settings 23 12 21 --plug_pairs AM FI NV PS TU WZ --message GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ"
    output = subprocess.getstatusoutput(command)[1]

    assert output.split('\n')[-1] == "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT"
