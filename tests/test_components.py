#!/usr/bin/env python3

from string import ascii_uppercase as alphabet

import pytest

from enigma import contains
from enigma.api.enigma_api import EnigmaAPI
from enigma.core.components import UKWD, Enigma, Plugboard, Uhr


def test_single_encrypt():
    enigma = EnigmaAPI.generate_component("Enigma I", "rotors", "I")

    assert enigma.forward("A") == "E"
    enigma.rotate()
    assert enigma.forward("A") == "J"
    enigma.rotate()
    assert enigma.forward("A") == "K"

    # "Looping back" to position 0 should produce the same result as in default position
    enigma.rotate(24)
    assert enigma.forward("A") == "E"


def test_ukwd():
    pairs = [
        "HK",
        "GL",
        "NQ",
        "SV",
        "UX",
        "TZ",
        "RW",
        "AD",
        "BF",
        "CO",
        "EP",
        "IM",
    ]
    ukwd = UKWD(pairs)

    assert ukwd.reflect("T") == "P"

    for pair in ukwd.wiring():
        assert contains(pairs, pair)


def test_uhr_addon():
    enigma = EnigmaAPI.generate_enigma(
        "Enigma M4", "UKW-b", ["Beta", "I", "II", "III"]
    )
    enigma.uhr('connect')
    enigma.uhr_position(3)
    enigma.plug_pairs(
        ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"]
    )
    setting = [3, 1, 1, 1]

    enigma.positions(setting)

    original = "TESTINGHOWUHRENCRYPTSTHISMESSAGE"

    output = ""
    for letter in original:
        output += enigma.press_key(letter)

    enigma.positions(setting)

    result = ""
    for letter in output:
        result += enigma.press_key(letter)

    assert result == original

    enigma.positions(setting)
    enigma.uhr_position(35)

    result = ""
    for letter in output:
        result += enigma.press_key(letter)

    assert result != original


def test_uhr_reciprocity():
    uhr = Uhr()
    uhr.pairs(["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"])

    # Reciprocal position testing
    for position in 0, 4, 8, 12, 16, 20, 24, 28, 32, 36:
        uhr.position(position)

        for ltr in alphabet:
            assert uhr.route(uhr.route(ltr), True) == ltr


def test_routing():
    """
    Tests if the forward routing is being routed correctly in the opposite direction (taking the
    relative rotor position into account)
    """
    rotor = EnigmaAPI.generate_component("Enigma I", "rotors", "I")

    for i in 1, 3, -2, 5, 7, 20:
        for letter in alphabet:
            assert letter == rotor.backward(
                rotor.forward(letter)
            ), "Backwards routing doesn't return to the original location!"
            rotor.rotate(i)


def test_implementation():
    """
    Tests t
he implementation by encrypting each letter of the alphabet
    4000 times and checking if the encrypted message does not contain the
    letter (this must always be true because the Enigma worked this way)

    The number of iterations is arbitrary (not to slow down the testing process)
    """
    enigma = EnigmaAPI.generate_enigma("Enigma M3", "UKW-B", ["I", "II", "III"])

    for letter in enigma.charset():
        for _ in range(1000):
            assert (
                enigma.press_key(letter) != letter
            ), "Enigma implementation wrong!"


@pytest.mark.parametrize(
    "offset_by, result",
    ((5, 6), (-1, 26), (26, 1), (15, 16), (50, 25), (-40, 13), (25, 26)),
)
def test_rotation(offset_by, result):
    enigma = EnigmaAPI.generate_component("Enigma I", "rotors", "I")
    enigma.rotate(offset_by)
    assert (
        enigma.offset() == result
    ), "Rotor offset is not being calculated correctly"


def test_position():
    rotor = EnigmaAPI.generate_component("Enigma I", "rotors", "I")

    rotor.rotate()
    assert rotor.position(True) == "02"
    assert rotor.position() == "B"
    rotor.rotate(20)
    assert rotor.position() == "V"


def test_reflector():
    reflector = EnigmaAPI.generate_component("Enigma M3", "reflectors", "UKW-B")

    result = reflector.reflect("A")
    assert "A" == reflector.reflect(result)


def test_turnover():
    enigma = EnigmaAPI.generate_component("Enigma M4", "rotors", "VI")

    for _ in range(50):
        if enigma.in_turnover():
            assert enigma.position() in enigma._turnover
        enigma.rotate()


def test_enigma():
    enigma = EnigmaAPI.generate_enigma("Enigma M3", "UKW-B", ["I", "II", "III"])

    result = ""
    for _ in "BDZGOW":
        result += enigma.press_key("A")

    assert result == "BDZGOW"


@pytest.mark.parametrize(
    "model, n_rotors, should_fail",
    (
        ("Enigma M4", 4, True),
        ("Enigma M3", 3, False),
        ("Enigma M3", 7, True),
        ("Enigma MX", 3, True),
        ("Enigma M3", 3, False),
        (33213, 3, True),
    ),
)
def test_enigma_models(model, n_rotors, should_fail):
    rotors = list(range(n_rotors))
    # Fake values instead of rotors because they are not needed in this test

    if should_fail:
        with pytest.raises(ValueError):
            EnigmaAPI.generate_enigma(model, "UKW-B", rotors)
    else:
        EnigmaAPI.generate_enigma(model, "UKW-B", rotors)


def test_plugboard():
    plugboard = Plugboard(["AB", "CD", "YZ"])

    assert plugboard.route("A") == "B"
    assert plugboard.route("B") == "A"
    assert plugboard.route("C") == "D"
    assert plugboard.route("D") == "C"
    assert plugboard.route("Y") == "Z"
    assert plugboard.route("Z") == "Y"
    assert plugboard.route("G") == "G"
    assert plugboard.route("I") == "I"


@pytest.mark.parametrize(
    "model, rotors, reflector, positions, ring_settings, plug_pairs, message, correct_result",
    (
        (  # Enigma instruction manual message
            "Enigma I",
            ("II", "I", "III"),
            "UKW-A",
            "ABL",
            (24, 13, 22),
            ("AM", "FI", "NV", "PS", "TU", "WZ"),
            "GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ",
            "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT",
        ),
        (  # Operation Barbarossa message 1
            "Enigma M3",
            ("II", "IV", "V"),
            "UKW-B",
            "BLA",
            (2, 21, 12),
            ("AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"),
            "EDPUDNRGYSZRCXNUYTPOMRMBOFKTBZREZKMLXLVEFGUEYSIOZVEQMIKUBPMMYLKLTTDEISMDICAGYKUACTCDOMOHWXMUUIAUBSTSLRNBZSZWNRFXWFYSSXJZVIJHIDISHPRKLKAYUPADTXQSPINQMATLPIFSVKDASCTACDPBOPVHJK",
            "AUFKLXABTEILUNGXVONXKURTINOWAXKURTINOWAXNORDWESTLXSEBEZXSEBEZXUAFFLIEGERSTRASZERIQTUNGXDUBROWKIXDUBROWKIXOPOTSCHKAXOPOTSCHKAXUMXEINSAQTDREINULLXUHRANGETRETENXANGRIFFXINFXRGTX",
        ),
        (  # Operation Barbarossa message 2
            "Enigma M3",
            ("II", "IV", "V"),
            "UKW-B",
            "LSD",
            (2, 21, 12),
            ("AV", "BS", "CG", "DL", "FU", "HZ", "IN", "KM", "OW", "RX"),
            "SFBWDNJUSEGQOBHKRTAREEZMWKPPRBXOHDROEQGBBGTQVPGVKBVVGBIMHUSZYDAJQIROAXSSSNREHYGGRPISEZBOVMQIEMMZCYSGQDGRERVBILEKXYQIRGIRQNRDNVRXCYYTNJR",
            "DREIGEHTLANGSAMABERSIQERVORWAERTSXEINSSIEBENNULLSEQSXUHRXROEMXEINSXINFRGTXDREIXAUFFLIEGERSTRASZEMITANFANGXEINSSEQSXKMXKMXOSTWXKAMENECXK",
        ),
        (  # Schranhorst
            "Enigma M3",
            ("III", "VI", "VIII"),
            "UKW-B",
            "UZV",
            (1, 8, 13),
            ("AN", "EZ", "HK", "IJ", "LR", "MQ", "OT", "PV", "SW", "UX"),
            "YKAENZAPMSCHZBFOCUVMRMDPYCOFHADZIZMEFXTHFLOLPZLFGGBOTGOXGRETDWTJIQHLMXVJWKZUASTR",
            "STEUEREJTANAFJORDJANSTANDORTQUAAACCCVIERNEUNNEUNZWOFAHRTZWONULSMXXSCHARNHORSTHCO",
        ),
        (  # U-264
            "Enigma M4",
            ("Beta", "II", "IV", "I"),
            "UKW-b",
            "VJNA",
            (1, 1, 1, 22),
            ("AT", "BL", "DF", "GJ", "HM", "NW", "OP", "QY", "RZ", "VX"),
            "NCZWVUSXPNYMINHZXMQXSFWXWLKJAHSHNMCOCCAKUQPMKCSMHKSEINJUSBLKIOSXCKUBHMLLXCSJUSRRDVKOHULXWCCBGVLIYXEOAHXRHKKFVDREWEZLXOBAFGYUJQUKGRTVUKAMEURBVEKSUHHVOYHABCJWMAKLFKLMYFVNRIZRVVRTKOFDANJMOLBGFFLEOPRGTFLVRHOWOPBEKVWMUQFMPWPARMFHAGKXIIBG",
            "VONVONJLOOKSJHFFTTTEINSEINSDREIZWOYYQNNSNEUNINHALTXXBEIANGRIFFUNTERWASSERGEDRUECKTYWABOSXLETZTERGEGNERSTANDNULACHTDREINULUHRMARQUANTONJOTANEUNACHTSEYHSDREIYZWOZWONULGRADYACHTSMYSTOSSENACHXEKNSVIERMBFAELLTYNNNNNNOOOVIERYSICHTEINSNULL",
        ),
    ),
)
def test_historical_messages(
    model,
    rotors,
    reflector,
    positions,
    ring_settings,
    plug_pairs,
    message,
    correct_result,
):
    # Enigma instruction manual message
    enigma = EnigmaAPI.generate_enigma(model, reflector, rotors)
    enigma.positions(positions)
    enigma.ring_settings(ring_settings)
    enigma.plug_pairs(plug_pairs)

    result = ""
    for letter in message:
        result += enigma.press_key(letter)

    assert result == correct_result


def test_cli():
    import subprocess

    command = "./enigma.py -cs --model 'Enigma I' --rotors II I III --reflector UKW-A --positions A B L " \
              "--ring_settings 24 13 22 --plug_pairs AM FI NV PS TU WZ " \
              "--message GCDSEAHUGWTQGRKVLFGXUCALXVYMIGMMNMFDXTGNVHVRMMEVOUYFZSLRHDRRXFJWCFHUHMUNZEFRDISIKBGPMYVXUZ"
    output = subprocess.getoutput(command)
    assert output == "FEINDLIQEINFANTERIEKOLONNEBEOBAQTETXANFANGSUEDAUSGANGBAERWALDEXENDEDREIKMOSTWAERTSNEUSTADT"
