"""Benchmarks EnigmaAPI encryption speed with the theoretically
most heavy model and components."""
import logging
import time
from itertools import repeat

from enigma.api.enigma_api import EnigmaAPI


def benchmark(char_n=None):
    """Benchmarks Enigma encryption speed with
    the (theoretically) most performance heavy settings.
    :param char_n: {int} Number of characters to benchmark on
    """
    enigma = EnigmaAPI.generate_enigma("Enigma M4", "UKW-b", ["Beta", "I", "II", "III"])
    enigma.uhr("connect")
    enigma.uhr_position(3)
    enigma.plug_pairs(["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"])

    logging.info("Benchmarking encryption speed with Enigma M4 and Uhr...")
    if isinstance(char_n, int):
        char_n = (char_n,)
    else:
        char_n = [10 ** num for num in range(7)]
    for num in char_n:
        start = time.time()
        for letter in repeat("A", num):
            enigma.press_key(letter)
        end = time.time()

        output = "Total encryption time: %.5f seconds for %d letters..." % (
            end - start, num)
        logging.info(output)
        print(output)
