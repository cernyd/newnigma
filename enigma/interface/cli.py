import logging

from enigma.api.enigma_api import EnigmaAPI


def cli(enigma_api, args):
    """
    Starts command line interface that encrypts a message based on args
    :param enigma_api: {EnigmaAPI}
    :param args: Object containing parsed command line arguments
    """
    if not args.message:
        print("Supply message with --message MESSAGE argument!")
        logging.error("No message to encrypt, quitting...")
        exit(1)

    print(enigma_api)
    print("Encrypted message: ", "")
    for letter in args.message[0].upper():
        print(enigma_api.encrypt(letter), end="")
    logging.info("Successfully encrypted %d letters, quitting CLI mode..." % len(args.message[0]))
    print()
