from string import ascii_uppercase as ALPHABET


def contains(pairs, pair):
    """Checks if a pair is not already in pairs
    :param pairs: {iterable}
    :param pair: {str, iterable} "AB", ('A', 'B'), ...
    """
    return pair in pairs or pair[::-1] in pairs


def validate_pairs(pairs, name):
    pairs = pairs[::]
    if len(pairs) > 13:
        raise ValueError("Too many pairs!")

    while pairs:
        pair = pairs.pop()
        letters = ''.join(pairs)
        invalid_letters = pair[0] not in ALPHABET or pair[1] not in ALPHABET

        if pair[::-1] in pairs or pair in pairs:
            raise ValueError("Duplicate %s pair '%s'!" % (name, pair))

        if invalid_letters or pair[0] == pair[1] or len(pair) != 2:
            raise ValueError("Invalid %s pair '%s'!" % (name, str(pair)))

        if pair[0] in letters:
            raise ValueError("Duplicate letter '%s'!" % pair[0])

        if pair[1] in letters:
            raise ValueError("Duplicate letter '%s'!" % pair[1])


def convert_position(position, charset, name="component"):
    """Converts position that can come in one of 3 formats:
    1) integer -> returned
    2) number as string -> converted to integer and returned
    3) character as string -> converted by finding index in charset and returned +1
    :param position: {str or int} position to convert
    :param charset: {str} charset to find position index in
    :param name: {str} component name for error message
    """
    try:
        if isinstance(position, str):
            if position in charset:
                position = charset.index(position) + 1
            else:
                position = int(position)
    except (TypeError, ValueError, KeyError):
        raise ValueError("Invalid %s '%s'!" % (name, str(position)))

    return position
