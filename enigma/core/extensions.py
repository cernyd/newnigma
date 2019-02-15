class Uhr:
    def __init__(self):
        self._alphabet = "ABCDEFGHIJKLMNOPQRST"
        self._back_wiring = "NSLAJCTERGPIHKBMDOFQ"  # rest is unmapped
        self._front_wiring = "DOFQHSJMLENCPARKTIBG"

        self._pairs = []
        self._offset = 0  # Scrambler disc offset

    def rotate(self, offset_by=1):
        self._offset = (self._offset + offset_by) % 40

    def position(self, new_position=None):
        if new_position:
            self._offset = new_position % 40
        else:
            return self._offset

    def pairs(self, pairs=None):
        """
        Sets pairs
        """
        if pairs:
            if len(pairs) != 10:
                raise ValueError("Uhr allows only exactly 10 pairs to be "
                                 "plugged in at a time!")

            self._pairs = [''.join(pair) for pair in pairs]
        else:
            return self._pairs

    def route(self, letter, backwards=False):  # ! Refactor here!
        wiring = ''.join(self._pairs)

        if letter not in wiring:
            return letter
        else:
            abs_input = (wiring.index(letter) + self._offset) % 20

            if backwards:
                rel_result = self._alphabet.index(self._front_wiring[abs_input])
            else:
                rel_result = self._alphabet.index(self._back_wiring[abs_input])

            return wiring[(rel_result - self._offset) % 20]
