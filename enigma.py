#!/usr/bin/env python3
"""Entrypoint into the Enigma simulation, processes command line arguments
and evaluates launch mode based upon them. Can launch in cli or gui mode.
Can read message data from stdin pipes."""

import argparse
import logging
from json import JSONDecodeError
from sys import stdin

from pytest import main as pytest_main

from benchmark import benchmark
from enigma.api.enigma_api import \
    EnigmaAPI  # pylint: disable=no-name-in-module
from enigma.core.components import \
    HISTORICAL  # pylint: disable=no-name-in-module
from enigma.interface.cli import cli
from enigma.interface.gui.gui import runtime
from enigma.utils.cfg_handler import load_config

DEFAULT_INIT = {"model": "Enigma I", "rotors": ["I", "II", "III"], "reflector": "UKW-A"}


def config_from_args(args, load_to=None):
    """Returns dictionary of options aquired from args
    :param args: argparse object with config
    :param load_to: {EnigmaAPI} EnigmaAPI to load the config to
    """
    config = {}
    model = args.model
    if model:
        model = model[0]
        config["model"] = model
        if load_to:
            load_to.model(model)
    else:
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
        config["ring_settings"] = args.ring_settings
        if load_to:
            load_to.ring_settings(config["ring_settings"])

    if args.reflector_position:
        config["reflector_position"] = args.reflector_position[0]
        if load_to:
            load_to.reflector_position(config["reflector_position"])

    if args.reflector_pairs:
        config["reflector_pairs"] = args.reflector_pairs
        if load_to:
            load_to.reflector_pairs(config["reflector_pairs"])

    if args.uhr:
        config["uhr_position"] = args.uhr[0]
        if load_to:
            load_to.uhr("connect")
            load_to.uhr_position(config["uhr_position"])

    if args.plug_pairs:
        config["plug_pairs"] = args.plug_pairs
        if load_to:
            load_to.plug_pairs(config["plug_pairs"])

    return config


def resolve_conflicts(args):
    """Resolves conflicting cli options"""
    if args.run_tests and args.only_run_tests:
        logging.error("Cannot run both --test and -T at once!")
        logging.shutdown()
        exit(1)

    if args.silent and args.verbose:
        logging.error("Conflicting flags --verbose and --silent!")
        print("Conflicting flags --verbose and --silent!")
        logging.shutdown()
        exit(-1)

    if args.silent and not args.cli:
        logging.error("Silent mode not available for graphical mode!")
        print("Silent mode not available for graphical mode!")
        logging.shutdown()
        exit(-1)


if __name__ == "__main__":
    # FLAG ARGS ====================================================
    PARSER = argparse.ArgumentParser(
        description="returns Enigma encrypted text base"
        "on settings and provided text."
    )

    ARGUMENT_DATA = (
        (
            ("-t", "--test"),
            dict(
                help="runs tests before launching the simulator to"
                "ensure it works correctly",
                dest="run_tests",
            ),
        ),
        (
            ("-T",),
            dict(
                help="runs tests with detailed stack traces and quits",
                dest="only_run_tests",
            ),
        ),
        (
            ("-c", "--cli"),
            dict(help="launches the simulator in the command line mode", dest="cli"),
        ),
        (("-p", "--preview"), dict(help="Runs a sample cli command")),
        (("-v", "--verbose"), dict(help="Turns on verbose logging messages")),
        (("-s", "--silent"), dict(help="Turns off all prints except cli output")),
    )
    for arg in ARGUMENT_DATA:
        PARSER.add_argument(*arg[0], **arg[1], action="store_true", default=False)

    PARSER.add_argument(
        "-b",
        "--benchmark",
        help="benchmarks encryption speed for N characters",
        nargs=1,
        dest="benchmark_n",
        metavar="N",
    )

    # SETTINGS ARGS ====================================================

    CLI_ARGS = PARSER.add_argument_group("startup settings")
    CLI_DATA = (
        (
            ("--from",),
            dict(help="file to load Enigma settings from", nargs=1, dest="filename"),
        ),
        (
            ("--model",),
            dict(
                help="available Enigma models: %s" % ", ".join(HISTORICAL.keys()),
                nargs=1,
                dest="model",
            ),
        ),
        (
            ("--rotors",),
            dict(help="rotors that will be used", nargs="+", metavar="rotor"),
        ),
        (
            ("--positions",),
            dict(
                help="starting rotor positions",
                nargs="+",
                default=None,
                metavar="position",
            ),
        ),
        (
            ("--ring_settings",),
            dict(
                help="rotor ring settings",
                nargs="+",
                default=None,
                metavar="ring_setting",
            ),
        ),
        (("--reflector",), dict(help="reflector that will be used", nargs=1)),
        (
            ("--reflector_position",),
            dict(
                help="reflector position (only available in EnigmaD, Enigma K,"
                "SwissK, EnigmaG, Railway, Tirpitz)",
                nargs=1,
                default=None,
                metavar="position",
            ),
        ),
        (
            ("--reflector_pairs",),
            dict(
                help="reflector wiring pairs for UKW-D (pairs do not "
                "correspond with real wiring!)",
                nargs="*",
                default=None,
                metavar="pair",
            ),
        ),
        (
            ("--plug_pairs",),
            dict(
                help="letter pairs to connect in the plugboard",
                nargs="*",
                default=None,
                metavar="pair",
            ),
        ),
        (
            ("--uhr",),
            dict(
                help="connects uhr to plugboard and sets position",
                nargs=1,
                default=None,
                metavar="position",
            ),
        ),
        (
            ("-m", "--message"),
            dict(help="text for encryption in cli mode", nargs=1, dest="message"),
        ),
    )

    for arg in CLI_DATA:
        CLI_ARGS.add_argument(*arg[0], **arg[1])

    # ARG PARSE ====================================================

    ARGS = PARSER.parse_args()

    # PRE-LAUNCH ACTIONS ===========================================

    if ARGS.verbose and not ARGS.silent:  # Set verbose logs
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s:%(module)s:%(funcName)s: %(message)s",
        )
    else:  # Disable logs (only show critical)
        logging.basicConfig(level=logging.CRITICAL)

    resolve_conflicts(ARGS)  # Checks for conflicting options

    # TEST PHASE ==================================================

    if ARGS.run_tests:
        logging.info("Running pre-launch tests...")
        # -x = stop at first failure
        EXIT_CODE = pytest_main(["tests", "-x", "--tb=no", "-s"])

        if EXIT_CODE != 1:
            logging.error("Pre-launch tests failed! Aborting...")
            logging.shutdown()
            exit(EXIT_CODE)

        logging.info("All pre-launch tests succeeded...")
    elif ARGS.only_run_tests:
        logging.info("Running tests with detailed feedback...")
        logging.shutdown()
        exit(pytest_main(["tests", "--tb=long", "--durations=3", "-s"]))

    # BENCHMARK ===========================================================

    if ARGS.benchmark_n:
        try:
            N_LETTERS = int(ARGS.benchmark_n[0])
        except ValueError:
            logging.error('Invalid number "%s" for benchmark, exiting...', str(N_LETTERS))
            print('Invalid number "%s", choose a valid number greater than 0!' % str(N_LETTERS))
            exit(1)

        if N_LETTERS <= 0:
            logging.error("Benchmark character count is not greater than 0, exiting...")
            print("Benchmark character count must be greater than 0!")
            exit(1)

        benchmark(N_LETTERS)
        logging.shutdown()
        exit()

    # CONFIG LOAD =========================================================

    logging.info("Loading config...")
    ENIGMA_API = EnigmaAPI(**DEFAULT_INIT)  # Fallback configuration
    CONFIG = config_from_args(ARGS)

    FILENAME = None
    if ARGS.filename:
        FILENAME = ARGS.filename[0]

    HAS_CONFIG = any(CONFIG.values())
    if HAS_CONFIG and FILENAME:
        print("Cannot load settings both from arguments and file!")
        exit(1)

    if HAS_CONFIG:  # Load from settings arguments
        if not CONFIG["model"] and len(CONFIG) > 1:
            print("Enigma model must be specified when specifying settings!")
            exit(1)

        try:
            config_from_args(ARGS, ENIGMA_API)
        except (KeyError, ValueError) as err:
            print(err)
            exit(1)

        logging.info("Loading settings specified in cli arguments...")
    elif FILENAME:  # Load from file specified in --from
        try:
            ENIGMA_API.load_from(FILENAME)
        except FileNotFoundError:
            msg = "No configuration file '%s' found!" % FILENAME
            logging.info(msg)
            print(msg)
            exit(1)
        except JSONDecodeError:
            msg = "Configuration file '%s'! is not of JSON format!" % FILENAME
            logging.info(msg)
            print(msg)
            exit(1)
        except KeyError:
            msg = "Configuration file '%s' loaded but did not contain required data!" % FILENAME
            logging.info(msg)
            print(msg)
            exit(1)

    else:  # Load defalt config
        try:
            ENIGMA_API = EnigmaAPI(**load_config("config.json")["default"])
        except (FileNotFoundError, KeyError, ValueError):
            logging.info(
                "Failed to load default config, using builtin defaults instead..."
            )

    # APPLICATION INIT ====================================================

    logging.info("Starting Enigma...")

    if ARGS.cli:  # Command line mode
        logging.info("Loading in CLI mode with settings:\n%s...", str(ENIGMA_API))

        # If stdin exists, load text from it
        MESSAGE = None if stdin.isatty() else str(stdin.readline()).strip()

        if MESSAGE is not None:
            logging.info("Loaded input '%s' from stdin...", MESSAGE)

        cli(ENIGMA_API, ARGS, MESSAGE)

    elif ARGS.preview:  # Preview command only
        logging.info("Printing preview...")
        print(
            "Copy the command below:\n\n./enigma.py --cli --model 'Enigma I' "
            "--rotors II I III --reflector UKW-A "
            "--message THISISANENIGMASAMPLEMESSAGE"
        )
    else:  # Graphical mode
        logging.info("Launching Enigma Qt Application...")
        runtime(ENIGMA_API)

    # APPLICATION SHUTDOWN =================================================

    logging.info("Program terminated...")
    logging.shutdown()
