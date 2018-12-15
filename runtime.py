#!/usr/bin/env python3

import argparse
import pytest
from v2.enigma.components import *

parser = argparse.ArgumentParser(description="returns Enigma encrypted text base on settings and provided text.")
parser.add_argument('--test', help="runs tests before launching the simulator to ensure it works correctly",
                    action="store_true", default=False, dest="run_tests")
parser.add_argument('--cli', help="launches the simulator in the command line mode", action='store_true', default=False,
                    dest='cli')

cli = parser.add_argument_group('arguments for cli mode')
cli.add_argument('--model', help="available Enigma models: Enigma1, EnigmaM3, EnigmaM4, " \
                                 "Norenigma, EnigmaG, EnigmaD, EnigmaK, SwissK, Railway, Tirpitz", nargs=1, dest='model', required=True)
cli.add_argument('--rotors', help="rotors that will be used", nargs=3, dest='rotors', required=True, metavar='rotor')
cli.add_argument('--positions', help='starting rotor positions', nargs=3, dest='positions', default=None, metavar='position')
cli.add_argument('--ring_settings', help='rotor ring settings', nargs=3, dest='ring_settings', default=None, metavar='ring_setting')
cli.add_argument('--reflector', help="reflector that will be used", nargs=1, dest='reflector', required=True)
cli.add_argument('--plug_pairs', help="letter pairs to connect in the plugboard", nargs='*', dest='plug_pairs', default=None, metavar='pair')
cli.add_argument('--message', help="message to be encrypted", nargs=1, dest='message', required=True)

import sys
from PyQt5 import QtGui, QtWidgets


if __name__ == '__main__':
    args = parser.parse_args()

    if args.run_tests:
        print('Running pre-launch tests...')
        pytest.main(['tests'])
    print('Starting newnigma...')

    if args.cli:
        print('Launching Enigma in the command line')
        model = args.model[0]
        rotors = args.rotors
        reflector = args.reflector[0]

        enigma = init_enigma(model, rotors, reflector)

        if args.positions is not None:
            enigma.positions = args.positions
        if args.ring_settings is not None:
            enigma.ring_settings = map(int, args.ring_settings)
        if args.plug_pairs is not None:
            enigma.set_plug_pairs(args.plug_pairs)

        print(enigma)

        print("Encrypted message:")
        for letter in args.message[0]:
            print(enigma.press_key(letter), end='')

        print()
