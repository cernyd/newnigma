#!/usr/bin/env python3
# pylint: disable=inconsistent-return-statements
"""Uhr extension device that attaches to the Enigmas plugboard"""

from enigma.core import ALPHABET, convert_position, validate_pairs


class Uhr:
    """Uhr Plugboard extension device"""

    def __init__(self):
        # Way contacts 00 ... 39 are steckered with the A board
        self.__contacts = [
            26, 11, 24, 21, 2, 31, 0, 25, 30, 39, 28, 13, 22, 35,
            20, 37, 6, 23, 4, 33, 34, 19, 32, 9, 18, 7, 16, 17, 10,
            3, 8, 1, 38, 27, 36, 29, 14, 15, 12, 5
        ]

        # The first contact of each plug hole (1a, 2a, 3a, ...)
        self.__a_pairs = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
        # The first contact of each plug hole (1b, 2b, 3b, ...)
        self.__b_pairs = [4, 16, 28, 36, 24, 12, 0, 8, 20, 32]

        self.__pairs = []
        self.__real_coords = []

        self.__offset = 0  # Scrambler disc offset

    def rotate(self, rotate_by=1):
        """Rotates Uhr dial by select number of positions
        :param rotate_by: {int} By how many positions
        """
        self.__offset = (self.__offset + rotate_by) % 40

    def position(self, new_position=None):
        """Positions getter/setter, valid position range is 00 - 39"""
        if new_position is not None:
            new_position = convert_position(new_position, ALPHABET, "Uhr position")

            if new_position not in range(0, 40):
                raise ValueError("Uhr positions can only be set to values 00 - 39!")

            self.__offset = new_position
        else:
            return self.__offset

    def pairs(self, pairs=None):
        """Pairs getter/setter, only 10 letter pairs can be connected at a time!"""
        if pairs is not None:
            pairs = [pair.upper() for pair in pairs]

            validate_pairs(pairs, "Uhr")

            if pairs and len(pairs) != 10:
                raise ValueError(
                    "Uhr allows only exactly 10 pairs to be plugged in at a time!"
                )

            self.__pairs = pairs

            a_coords = []
            b_coords = []
            for i, pair in enumerate(self.__pairs):
                a_coords.append(("a", pair[0], self.__a_pairs[i], self.__a_pairs[i] + 2))
                b_coords.append(("b", pair[1], self.__b_pairs[i], self.__b_pairs[i] + 2))
            self.__real_coords = {"a": a_coords, "b": b_coords}
        else:
            return self.__pairs

    def route(self, letter, backwards=False):
        """Routes letters trough the Uhr
        :param letter: {str} Letter to route
        :param backwards: {bool} Letters are wired differently
                          if backwards is True (returning from rotor assembly)
        """
        board = None
        for plug in self.__real_coords["a"] + self.__real_coords["b"]:
            if plug[1] == letter:
                board = "a" if plug[0] == "b" else "b"
                send_pin = (plug[3 if backwards else 2] + self.__offset) % 40
                break

        if board == "a":
            receive_pin = self.__contacts[send_pin]
        elif board == "b":
            receive_pin = self.__contacts.index(send_pin)
        else:
            return letter  # Unconnected pairs are not routed

        receive_pin = (receive_pin - self.__offset) % 40

        index = 2 if backwards else 3
        for plug in self.__real_coords[board]:
            if plug[index] == receive_pin:
                return plug[1]
