#!/usr/bin/env python3

import argparse
import logging

import pytest

from enigma.api.enigma_api import EnigmaAPI
from enigma.core.components import historical
from enigma.interface.cli import cli
from enigma.interface.gui.gui import Runtime
from enigma.utils.cfg_handler import load_config
from benchmark import benchmark


def extract_settings(args):
    pass


if __name__ == "__main__":
    # ====================================================
    # MAIN PARSER GROUP
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
        (("-v", "--verbose"), dict(help="Turns on verbose logging messages"))
    )
    for arg in argument_data:
        parser.add_argument(*arg[0], **arg[1], action="store_true", default=False)

    parser.add_argument("-b", "--benchmark", help="benchmarks encryption speed for N letters",
                        nargs=1, dest="benchmark_n", metavar="N")

    # ====================================================
    # CLI GROUP

    cli_args = parser.add_argument_group("arguments for cli mode")
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
        (("-m", "--message"), dict(help="message to be encrypted", nargs=1, dest="message")),
    )

    for arg in cli_data:
        cli_args.add_argument(*arg[0], **arg[1])

    # ARG PARSE ====================================================

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(module)s:%(funcName)s: %(message)s")
    else:
        logging.basicConfig(level=logging.CRITICAL)

    if args.run_tests and args.only_run_tests:
        logging.error("Cannot run both --test and -T at once!")
        logging.shutdown()
        exit(1)

    if args.run_tests:
        logging.info("Running pre-launch tests...")
        exit_code = pytest.main(["tests", "-x", "--tb=no"])  # -x = stop at first failure

        if exit_code == 1:
            logging.error("Pre-launch tests failed! Aborting...")
            logging.shutdown()
            exit(1)
        logging.info("All pre-launch tests succeeded...")
    elif args.only_run_tests:
        logging.info("Running tests with detailed feedback...")
        logging.shutdown()
        exit(pytest.main(["tests", "--tb=long", "--durations=3"]))

    if args.benchmark_n:
        try:
            n = int(args.benchmark_n[0])
        except ValueError:
            logging.error('Invalid number "%s" for benchmark, exiting...' % str(n))
            print('Invalid number "%s", choose a valid number greater than 0!' % str(n))
            exit(1)

        if not n > 0:
            logging.error('Benchmark letter count is not greater than 0, exiting...')
            print('Benchmark letter count must be greater than 0!')
            exit(1)

        benchmark(n)
        logging.shutdown()
        exit()

    # CONFIG LOAD ====================================================

    logging.info("Loading config...")
    data = None
    try:
        data = load_config("config.json")["default"]
    except Exception:
        logging.shutdown()
        exit(1)

    # APPLICATION INIT ====================================================
    # LOADS EITHER CLI OR GUI BASED ON COMMAND LINE ARG

    logging.info("Starting Enigma...")

    enigma_api = EnigmaAPI(data["model"], data["reflector"], data["rotors"])

    if args.cli:
        logging.info("Loading in CLI mode with settings:\n%s..." % str(enigma_api))
        cli(enigma_api, args)
    elif args.preview:
        logging.info("Printing preview...")
        print(
            "Copy the command below:\n\n./enigma.py --cli --model 'Enigma I' "
            "--rotors II I III --reflector UKW-A "
            "--message THISISANENIGMASAMPLEMESSAGE"
        )
    else:
        logging.info("Launching Enigma Qt Application...")
        Runtime(enigma_api)

    logging.info("Program terminated...")
    logging.shutdown()
