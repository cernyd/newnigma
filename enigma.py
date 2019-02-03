#!/usr/bin/env python3

import argparse
import pytest
from enigma.utils.cfg_handler import Config
from enigma.interface.gui.gui import Runtime
from enigma.interface.cli import cli
from enigma.api.enigma_api import EnigmaAPI
import logging


if __name__ == '__main__':
    # ====================================================
    # MAIN PARSER GROUP
    parser = argparse.ArgumentParser(description="returns Enigma encrypted text base on settings and provided text.")

    argument_data = (
        ('--test', dict(help="runs tests before launching the simulator to ensure it works correctly", dest="run_tests")),
        ('--cli', dict(help="launches the simulator in the command line mode", dest='cli')),
        ('--preview', dict(help="Runs a sample cli command")),
        ('--verbose', dict(help="Turns on verbose logging messages"))
    )
    for arg in argument_data:
        parser.add_argument(arg[0], **arg[1], action="store_true", default=False)

    # ====================================================
    # CLI GROUP

    cli_args = parser.add_argument_group('arguments for cli mode')
    cli_data = (
        ('--model', dict(help="available Enigma models: Enigma1, EnigmaM3, EnigmaM4, " \
              "Norenigma, EnigmaG, EnigmaD, EnigmaK, SwissK, Railway, Tirpitz", nargs=1, dest='model')),
        ('--rotors', dict(help="rotors that will be used", nargs='+', metavar='rotor')),
        ('--positions', dict(help="starting rotor positions", nargs='+', default=None, metavar='position')),
        ('--ring_settings', dict(help="rotor ring settings", nargs='+', default=None, metavar='ring_setting')),
        ('--reflector', dict(help="reflector that will be used", nargs=1)),
        ('--reflector_position', dict(help="reflector position (only available in EnigmaD, EnigmaK, SwissK, EnigmaG, Railway, Tirpitz)", nargs=1, default=None, metavar='position')),
        ('--reflector_pairs', dict(help="reflector wiring pairs for UKW-D (pairs do not correspond with real wiring!)", nargs='*', default=None, metavar='pair')),
        ('--plug_pairs', dict(help="letter pairs to connect in the plugboard", nargs='*', default=None, metavar='pair')),
        ('--uhr', dict(help="connects uhr to plugboard and sets position", nargs=1, default=None, metavar='position')),
        ('--message', dict(help="message to be encrypted", nargs=1, dest='message'))
    )

    for arg in cli_data:
        cli_args.add_argument(arg[0], **arg[1])

    # ARG PARSE ====================================================
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.run_tests:
        logging.info('Running pre-launch tests...')
        pytest.main(['tests'])

    # CONFIG LOAD ====================================================

    logging.info("Loading config...")
    cfg = Config("config.json")
    cfg.mk_cache()
    data = cfg.cache['default']

    # APPLICATION INIT ====================================================
    # LOADS EITHER CLI OR GUI BASED ON COMMAND LINE ARG
    logging.info('Starting newnigma...')

    enigma_api = EnigmaAPI(data['model'], data['reflector'], data['rotors'])

    if args.cli:
        cli(enigma_api, args)
    elif args.preview:
        print("Copy the command below:\n\n./enigma.py --cli --model Enigma1 --rotors II I III " \
              "--reflector UKW-A --message THISISANENIGMASAMPLEMESSAGE")
        exit()
    else:
        logging.info('Launching newnigma Qt Application...')
        runtime = Runtime(enigma_api, cfg.load, cfg.save)
        runtime.run()

