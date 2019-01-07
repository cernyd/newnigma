#!/usr/bin/env python3

import argparse
import pytest
from v2.newnigma.components import *
from v2.cfg_handler import Config
from v2.gui import Runtime
import logging


# ====================================================
# MAIN PARSER GROUP
parser = argparse.ArgumentParser(description="returns Enigma encrypted text base on settings and provided text.")
parser.add_argument('--test', help="runs tests before launching the simulator to ensure it works correctly",
                    action="store_true", default=False, dest="run_tests")
parser.add_argument('--cli', help="launches the simulator in the command line mode", action='store_true', default=False,
                    dest='cli')
parser.add_argument('--preview', help="Runs a sample cli command", action='store_true', default=False)
parser.add_argument('--cli_default', help="Loads cli encryption with default settings from config file", dest='cli_default', action='store_true', default=False)
parser.add_argument('--verbose', help="Turns on verbose logging messages", dest='verbose', action='store_true', default=False)

# ====================================================
# CLI GROUP
cli = parser.add_argument_group('arguments for cli mode')
cli.add_argument('--model', help="available Enigma models: Enigma1, EnigmaM3, EnigmaM4, " \
                                 "Norenigma, EnigmaG, EnigmaD, EnigmaK, SwissK, Railway, Tirpitz", nargs=1, dest='model')
cli.add_argument('--rotors', help="rotors that will be used", nargs=3, dest='rotors', metavar='rotor')
cli.add_argument('--positions', help='starting rotor positions', nargs=3, dest='positions', default=None, metavar='position')
cli.add_argument('--ring_settings', help='rotor ring settings', nargs=3, dest='ring_settings', default=None, metavar='ring_setting')
cli.add_argument('--reflector', help="reflector that will be used", nargs=1, dest='reflector')
cli.add_argument('--plug_pairs', help="letter pairs to connect in the plugboard", nargs='*', dest='plug_pairs', default=None, metavar='pair')
cli.add_argument('--message', help="message to be encrypted", nargs=1, dest='message', default=None)
# ====================================================


if __name__ == '__main__':
    # ====================================================
    # ARG PARSE
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.cli_default:  # CLI DEFAULT SETTINGS
        args.cli = True
    if args.run_tests:
        logging.info('Running pre-launch tests...')
        pytest.main(['tests'])

    # ====================================================
    # CONFIG LOAD

    logging.info("Loading config...")
    cfg = Config("data/config.json")
    cfg.mk_cache()

    # ====================================================
    # APPLICATION INIT
    # LOADS EITHER CLI OR GUI BASED ON COMMAND LINE ARG
    logging.info('Starting newnigma...')

    if args.preview:
        print("Copy the command below:\n\n./newnigma.py --cli --model Enigma1 --rotors II I III " \
              "--reflector UKW-A --message THISISANENIGMASAMPLEMESSAGE")
        exit()

    if args.cli:
        if args.cli_default:  # CLI DEFAULT SETTINGS
            logging.info("Loading cli defaults...")
            data = cfg.cache['cli_default']
            enigma = init_enigma(data['model'], data['rotors'], data['reflector'])

        else:  # CLI MANUAL SETTINGS
            logging.info('Launching newnigma in the command line...')
            if not any((args.model, args.rotors, args.reflector)):
                print("Must supply --model, --rotors, --reflector!")
                exit(-1)

            model = args.model[0]
            rotors = args.rotors
            reflector = args.reflector[0]

            enigma = init_enigma(model, rotors, reflector)

        if not args.message:
            print("Supply message with --message MESSAGE argument!")
            exit(-1)

        if args.positions is not None:
            enigma.positions = args.positions
        if args.ring_settings is not None:
            enigma.ring_settings = map(int, args.ring_settings)
        if args.plug_pairs is not None:
            enigma.set_plug_pairs(args.plug_pairs)

        print(enigma)
        print("Encrypted message:")

        for letter in args.message[0].upper():
            print(enigma.press_key(letter), end='')

        print()
    else:
        logging.info('Launching newnigma Qt Application...')
        runtime = Runtime()
        runtime.run()
    # ====================================================

