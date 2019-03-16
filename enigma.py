#!/usr/bin/env python3

import argparse
import logging
from sys import stdin

import pytest
from benchmark import benchmark
from enigma.api.enigma_api import EnigmaAPI
from enigma.core.components import historical
from enigma.interface.cli import cli
from enigma.interface.gui.gui import Runtime
from enigma.utils.cfg_handler import load_config

default_init = {
    "model": "Enigma I",
    "rotors": ["I", "II", "III"],
    "reflector": "UKW-A"
}


def config_from_args(args, load_to=None):
    """Returns dictionary of options aquired from args
    :param args: argparse object with config
    :param load_to: {EnigmaAPI} EnigmaAPI to load the config to
    """
    config = {}

    try:
        config["model"] = args.model[0]
        if load_to:
            load_to.model(config["model"])
    except Exception:
        config["model"] = None

    if args.reflector:
        config["reflector"] = args.reflector[0]
        if load_to:
            load_to.reflector(config["reflector"])

    if args.rotors:
        config["rotors"] = args.rotors
        if load_to:
            load_to.rotors(config["rotors"])

    if args.positions:
        config["positions"] = args.positions
        if load_to:
            load_to.positions(config["positions"])

    if args.ring_settings:
        config["ring_settings"] = map(int, args.ring_settings)
        if load_to:
            load_to.ring_settings(config["ring_settings"])

    if args.reflector_position:
        config["reflector_position"] = int(args.reflector_position[0])
        if load_to:
            load_to.ring_settings(config["reflector_position"])

    if args.reflector_pairs:
        config["reflector_wiring"] = args.reflector_pairs
        if load_to:
            load_to.ring_settings(config["reflector_wiring"])

    if args.uhr:
        config["uhr_position"] = int(args.uhr[0])
        if load_to:
            load_to.ring_settings(config["uhr_position"])

    if args.plug_pairs:
        config["plug_pairs"] = args.plug_pairs
        if load_to:
            load_to.ring_settings(config["plug_pairs"])

    return config


def resolve_conflicts(args):
    """Resolves conflicting cli options"""
    if args.run_tests and args.only_run_tests:
        logging.error("Cannot run both --test and -T at once!")
        logging.shutdown()
        exit(1)

    if args.silent and args.verbose:
        logging.error("Conflicting flags --verbose and --silent!")
        print("conflicting flags --verbose and --silent!")
        logging.shutdown()
        exit(-1)

    if args.silent and not args.cli:
        logging.error("Silent mode not available for graphical mode!")
        print("Silent mode not available for graphical mode!")
        logging.shutdown()
        exit(-1)


if __name__ == "__main__":
    # FLAG ARGS ====================================================
    parser = argparse.ArgumentParser(
        description="returns Enigma encrypted text base"
        "on settings and provided text."
    )

    argument_data = (
        (
            ("-t", "--test"),
            dict(
                help="runs tests before launching the simulator to"
                "ensure it works correctly",
                dest="run_tests",
            ),
        ),
        (
            ("-T", ),
            dict(
                help="runs tests with detailed stack traces and quits",
                dest="only_run_tests"
            ),
        ),
        (
            ("-c", "--cli"),
            dict(help="launches the simulator in the command line mode", dest="cli"),
        ),
        (("-p", "--preview"), dict(help="Runs a sample cli command")),
        (("-v", "--verbose"), dict(help="Turns on verbose logging messages")),
        (("-s", "--silent"), dict(help="Turns off all prints except cli output"))
    )
    for arg in argument_data:
        parser.add_argument(*arg[0], **arg[1], action="store_true", default=False)

    parser.add_argument("-b", "--benchmark", help="benchmarks encryption speed for N characters",
                        nargs=1, dest="benchmark_n", metavar="N")

    # SETTINGS ARGS ====================================================

    cli_args = parser.add_argument_group("startup settings")
    cli_data = (
        (
            ("--from", ),
            dict(
                help="file to load Enigma settings from",
                nargs=1,
                dest="filename"
            )
        ),
        (
            ("--model", ),
            dict(
                help="available Enigma models: %s" % ", ".join(historical.keys()),
                nargs=1,
                dest="model",
            ),
        ),
        (("--rotors", ), dict(help="rotors that will be used", nargs="+", metavar="rotor")),
        (
            ("--positions", ),
            dict(
                help="starting rotor positions",
                nargs="+",
                default=None,
                metavar="position",
            ),
        ),
        (
            ("--ring_settings", ),
            dict(
                help="rotor ring settings",
                nargs="+",
                default=None,
                metavar="ring_setting",
            ),
        ),
        (("--reflector", ), dict(help="reflector that will be used", nargs=1)),
        (
            ("--reflector_position", ),
            dict(
                help="reflector position (only available in EnigmaD, Enigma K,"
                "SwissK, EnigmaG, Railway, Tirpitz)",
                nargs=1,
                default=None,
                metavar="position",
            ),
        ),
        (
            ("--reflector_pairs", ),
            dict(
                help="reflector wiring pairs for UKW-D (pairs do not "
                "correspond with real wiring!)",
                nargs="*",
                default=None,
                metavar="pair",
            ),
        ),
        (
            ("--plug_pairs", ),
            dict(
                help="letter pairs to connect in the plugboard",
                nargs="*",
                default=None,
                metavar="pair",
            ),
        ),
        (
            ("--uhr", ),
            dict(
                help="connects uhr to plugboard and sets position",
                nargs=1,
                default=None,
                metavar="position",
            ),
        ),
        (("-m", "--message"), dict(help="text for encryption in cli mode", nargs=1, dest="message")),
    )

    for arg in cli_data:
        cli_args.add_argument(*arg[0], **arg[1])

    # ARG PARSE ====================================================

    args = parser.parse_args()

    # PRE-LAUNCH ACTIONS ===========================================

    if args.verbose and not args.silent:  # Set verbose logs
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s:%(module)s:%(funcName)s: %(message)s")
    else:  # Disable logs (only show critical)
        logging.basicConfig(level=logging.CRITICAL)

    resolve_conflicts(args)  # Checks for conflicting options

    # TEST PHASE ==================================================

    if args.run_tests:
        logging.info("Running pre-launch tests...")
        # -x = stop at first failure
        exit_code = pytest.main(["tests", "-x", "--tb=no"])

        if exit_code != 1:
            logging.error("Pre-launch tests failed! Aborting...")
            logging.shutdown()
            exit(exit_code)

        logging.info("All pre-launch tests succeeded...")
    elif args.only_run_tests:
        logging.info("Running tests with detailed feedback...")
        logging.shutdown()
        exit(pytest.main(["tests", "--tb=long", "--durations=3"]))

    # BENCHMARK ===========================================================

    if args.benchmark_n:
        try:
            n = int(args.benchmark_n[0])
        except ValueError:
            logging.error('Invalid number "%s" for benchmark, exiting...' % str(n))
            print('Invalid number "%s", choose a valid number greater than 0!' % str(n))
            exit(1)

        if not n > 0:
            logging.error('Benchmark character count is not greater than 0, exiting...')
            print('Benchmark character count must be greater than 0!')
            exit(1)

        benchmark(n)
        logging.shutdown()
        exit()

    # CONFIG LOAD =========================================================

    logging.info("Loading config...")
    enigma_api = EnigmaAPI(**default_init)  # Fallback configuration
    config = config_from_args(args)

    filename = None
    if args.filename:
        filename = args.filename[0]

    if config and filename:
        print("Cannot load settings both from arguments and file!")
        exit(1)

    if config:  # Load from settings arguments
        if not config["model"] and len(config) > 1:
            print("Enigma model must be specified when specifying settings!")
            exit(1)
        config_from_args(args, enigma_api)
        logging.info("Loading settings specified in cli arguments...")
    elif filename:  # Load from file specified in --from
        try:
            enigma_api.load_from(filename)
        except Exception:
            logging.info('No valid configuration found in "%s", using defaults instead....' % filename)
    else:  # Load defalt config
        try:
            enigma_api = EnigmaAPI(**load_config("config.json")["default"])
        except Exception:
            logging.info("Failed to load default config, using builtin defaults instead...")

    # APPLICATION INIT ====================================================

    logging.info("Starting Enigma...")

    if args.cli:  # Command line mode
        logging.info("Loading in CLI mode with settings:\n%s..." % str(enigma_api))

        # If stdin exists, load text from it
        msg = None if stdin.isatty() else str(stdin.readline()).strip()

        if msg is not None:
            logging.info("Loaded input '%s' from stdin..." % msg)

        cli(enigma_api, args, msg)

    elif args.preview:  # Preview command only
        logging.info("Printing preview...")
        print(
            "Copy the command below:\n\n./enigma.py --cli --model 'Enigma I' "
            "--rotors II I III --reflector UKW-A "
            "--message THISISANENIGMASAMPLEMESSAGE"
        )
    else:  # Graphical mode
        logging.info("Launching Enigma Qt Application...")
        Runtime(enigma_api)

    # APPLICATION SHUTDOWN =================================================

    logging.info("Program terminated...")
    logging.shutdown()
