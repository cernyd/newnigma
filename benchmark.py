import logging
import time
from itertools import repeat

from enigma.api.enigma_api import EnigmaAPI


def benchmark(char_n=None):
    """Benchmarks Enigma encryption speed with
    the (theoretically) most performance heavy settings.
    :param char_n: {int} Number of characters to benchmark on
    """
    enigma = EnigmaAPI.generate_enigma(
        "Enigma M4", "UKW-b", ["Beta", "I", "II", "III"]
    )
    enigma.uhr('connect')
    enigma.uhr_position(3)
    enigma.plug_pairs(
        ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"]
    )

    logging.info("Benchmarking encryption speed with Enigma M4 and Uhr...")
    if type(char_n) == int:
        char_n = (char_n, )
    else:
        char_n = [10**n for n in range(7)]
    for n in char_n:
        start = time.time()
        for letter in repeat("A", n):
            enigma.press_key(letter)
        end = time.time()

        output = "Total encryption time: %.5f seconds for %d letters..." % (end - start, n)
        logging.info(output)
        print(output)
