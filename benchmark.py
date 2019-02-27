from enigma.api.enigma_api import EnigmaAPI

import time
from itertools import repeat
import logging


enigma = EnigmaAPI.generate_enigma(
    "EnigmaM4", "UKW-b", ["Beta", "I", "II", "III"]
)
enigma.uhr('connect')
enigma.uhr_position(3)
enigma.plug_pairs(
    ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST"]
)

logging.info("Benchmarking encryption speed with EnigmaM4 and Uhr...")
for n in range(7):
    start = time.time()
    for letter in repeat("A", 10**n):
        enigma.press_key(letter)
    end = time.time()
    print("Total encryption time: %.5f seconds for %d letters..." % (end - start, 10**n))
