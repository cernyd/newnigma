#!/usr/bin/env python3
"""Other miscellaneous assets"""

def contains(pairs, pair):
    """Checks if a pair is not already in pairs
    :param pairs: {iterable}
    :param pair: {str, iterable} "AB", ('A', 'B'), ...
    """
    return pair in pairs or pair[::-1] in pairs
