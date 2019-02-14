class Uhr:
    def __init__(self):
        # Way contacts 00 ... 39 are steckered with the A board
        self.contacts = [
            26,
            11,
            24,
            21,
            2,
            31,
            0,
            25,
            30,
            39,
            28,
            13,
            22,
            35,
            20,
            37,
            6,
            23,
            4,
            33,
            34,
            19,
            32,
            9,
            18,
            7,
            16,
            17,
            10,
            3,
            8,
            1,
            38,
            27,
            36,
            29,
            14,
            15,
            12,
            5,
        ]

        # The first contact of each plug hole (1a, 2a, 3a, ...)
        self.a_pairs = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
        # The first contact of each plug hole (1b, 2b, 3b, ...)
        self.b_pairs = [4, 16, 28, 36, 24, 12, 0, 8, 20, 32]

        self._pairs = []

        self._offset = 0  # Scrambler disc offset

    def rotate(self, offset_by=1):
        self._offset = (self._offset + offset_by) % 40

    def position(self, new_position=None):
        if new_position is not None:
            self._offset = new_position % 40
        else:
            return self._offset

    def pairs(self, pairs=None):
        """
        Sets pairs
        """
        if pairs is not None:
            if len(pairs) != 10:
                raise ValueError("Uhr allows only exactly 10 pairs to be "
                                 "plugged in at a time!")
            self._pairs = pairs
        else:
            return self._pairs

    def route(self, letter, backwards=False):
        coords = []
        for i, pair in enumerate(self._pairs):
            coords.append(
                ("%da" % (i + 1), pair[0], self.a_pairs[i], self.a_pairs[i] + 2)
            )
            coords.append(
                ("%db" % (i + 1), pair[1], self.b_pairs[i], self.b_pairs[i] + 2)
            )

        board = None
        for plug in coords:
            if plug[1] == letter:
                board = "a" if "b" in plug[0] else "b"
                if backwards:
                    send_pin = (plug[3] + self._offset) % 40
                else:
                    send_pin = (plug[2] + self._offset) % 40
                break

        if board == "a":
            receive_pin = self.contacts[send_pin]
        elif board == "b":
            receive_pin = self.contacts.index(send_pin)
        else:
            return letter  # Unconnected pairs are not routed

        receive_pin = (receive_pin - self._offset) % 40

        for plug in coords:
            if board in plug[0]:
                if backwards:
                    if plug[2] == receive_pin:
                        return plug[1]
                else:
                    if plug[3] == receive_pin:
                        return plug[1]
