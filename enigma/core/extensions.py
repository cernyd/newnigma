#!/usr/bin/env python3
# pylint: disable=inconsistent-return-statements
"""Uhr extension device that attaches to the Enigmas plugboard"""


class Uhr:
    """Uhr Plugboard extension device"""

    def __init__(self):
        # Way contacts 00 ... 39 are steckered with the A board
        self.contacts = [
            26, 11, 24, 21, 2, 31, 0, 25, 30, 39, 28, 13, 22, 35,
            20, 37, 6, 23, 4, 33, 34, 19, 32, 9, 18, 7, 16, 17, 10,
            3, 8, 1, 38, 27, 36, 29, 14, 15, 12, 5
        ]

        # The first contact of each plug hole (1a, 2a, 3a, ...)
        self.a_pairs = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
        # The first contact of each plug hole (1b, 2b, 3b, ...)
        self.b_pairs = [4, 16, 28, 36, 24, 12, 0, 8, 20, 32]

        self._pairs = []
        self._real_coords = []

        self._offset = 0  # Scrambler disc offset

    def rotate(self, rotate_by=1):
        """Rotates Uhr dial by select number of positions
        :param rotate_by: {int} By how many positions
        """
        self._offset = (self._offset + rotate_by) % 40

    def position(self, new_position=None):
        """Positions getter/setter, valid position range is 00 - 39"""
        if isinstance(new_position, int):
            if new_position not in range(0, 40):
                raise ValueError("Positions can only be set to values 1 - 26!")
            self._offset = new_position
        else:
            return self._offset

    def pairs(self, pairs=None):
        """Pairs getter/setter, only 10 letter pairs can be connected at a time!"""
        if pairs is not None:
            if pairs and len(pairs) != 10:
                raise ValueError(
                    "Uhr allows only exactly 10 pairs to be plugged in at a time!"
                )
            self._pairs = pairs

            a_coords = []
            b_coords = []
            for i, pair in enumerate(self._pairs):
                a_coords.append(("a", pair[0], self.a_pairs[i], self.a_pairs[i] + 2))
                b_coords.append(("b", pair[1], self.b_pairs[i], self.b_pairs[i] + 2))
            self._real_coords = {"a": a_coords, "b": b_coords}
        else:
            return self._pairs

    def route(self, letter, backwards=False):
        """Routes letters trough the Uhr
        :param letter: {str} Letter to route
        :param backwards: {bool} Letters are wired differently
                          if backwards is True (returning from rotor assembly)
        """
        board = None
        for plug in self._real_coords["a"] + self._real_coords["b"]:
            if plug[1] == letter:
                board = "a" if plug[0] == "b" else "b"
                send_pin = (plug[3 if backwards else 2] + self._offset) % 40
                break

        if board == "a":
            receive_pin = self.contacts[send_pin]
        elif board == "b":
            receive_pin = self.contacts.index(send_pin)
        else:
            return letter  # Unconnected pairs are not routed

        receive_pin = (receive_pin - self._offset) % 40

        index = 2 if backwards else 3
        for plug in self._real_coords[board]:
            if plug[index] == receive_pin:
                return plug[1]
