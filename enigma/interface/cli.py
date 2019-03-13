import logging

from enigma.api.enigma_api import EnigmaAPI


def cli(enigma_api, args):
    """
    Starts command line interface that encrypts a message based on args
    :param enigma_api: {EnigmaAPI}
    :param args: Object containing parsed command line arguments
    """
    components = (args.model, args.reflector, args.rotors)

    if len(components) > 0 and not all(components):
        print("Must supply --model, --rotors, --reflector!")
        logging.error("model, rotor or reflector parameter not supplied, exiting with status code 1...")
        exit(1)
    elif len(components) > 0 and all(components):
        logging.info("All parameters found, trying to find message...")
        enigma_api = EnigmaAPI(*components)

    if not args.message:
        print("Supply message with --message MESSAGE argument!")
        logging.error("No message to encrypt, quitting...")
        exit(1)

    if args.model:
        enigma_api.model(args.model[0])
    if args.positions:
        enigma_api.positions(args.positions)
    if args.ring_settings:
        enigma_api.ring_settings(map(int, args.ring_settings))
    if args.reflector_position:
        enigma_api.reflector_position(int(args.reflector_position[0]))
    if args.reflector_pairs:
        enigma_api.reflector_pairs(args.reflector_pairs)
    if args.uhr:
        enigma_api.uhr('connect')
        enigma_api.uhr_position(int(args.uhr[0]))
    if args.plug_pairs:
        enigma_api.plug_pairs(args.plug_pairs)

    print(enigma_api)
    print("Encrypted message: ", "")
    for letter in args.message[0].upper():
        print(enigma_api.encrypt(letter), end="")
    logging.info("Successfully encrypted %d letters, quitting CLI mode..." % len(args.message[0]))
    print()
