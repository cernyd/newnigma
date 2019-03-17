#!/usr/bin/env python3
"""Command line mode of Enigma encryption, encrypts and displays message based on
supplied enigma_api object."""

import logging


def cli(enigma_api, args, msg=None):
    """Starts command line interface that encrypts a message based on args
    :param enigma_api: {EnigmaAPI}
    :param args: Object containing parsed command line arguments
    :param msg: {str} Message from stdin, will avoid -m error if supplied
    """
    if not args.message and msg is None:
        if not args.silent:
            print(
                "Supply message with --message MESSAGE argument or provide input trough stdin!"
            )
        logging.error("No message to encrypt, quitting...")
        exit(1)
    else:
        msg = (args.message[0] if msg is None else msg).upper()

    try:
        msg = enigma_api.encrypt(msg)
    except ValueError as err:
        print(err)
        exit(1)

    if not args.silent:
        print(enigma_api)
        print("Encrypted message: %s" % msg, end='')
    else:
        print(msg, end='')

    logging.info("Successfully encrypted %d letters, quitting CLI mode..." % len(msg))

    if not args.silent:
        print()
