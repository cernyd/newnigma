import logging

from enigma.api.enigma_api import EnigmaAPI


def cli(enigma_api, args, msg=None):
    """
    Starts command line interface that encrypts a message based on args
    :param enigma_api: {EnigmaAPI}
    :param args: Object containing parsed command line arguments
    """
    if not args.message and msg is None:
        if not args.silent:
            print("Supply message with --message MESSAGE argument or provide input trough stdin!")
        logging.error("No message to encrypt, quitting...")
        exit(1)
    else:
        if msg is None:
            msg = args.message[0].upper()
        else:
            msg = msg.upper()

    if not args.silent:
        print(enigma_api)
        print("Encrypted message: ", "")

    print(enigma_api.encrypt(msg), end='')
    logging.info("Successfully encrypted %d letters, quitting CLI mode..." % len(msg))

    if not args.silent:
        print()
