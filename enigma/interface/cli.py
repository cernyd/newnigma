import argparse
from enigma.api.enigma_api import EnigmaAPI
import logging


def cli(enigma_api, args):
    logging.info('Launching newnigma in the command line...')
    components = (args.model[0], args.reflector[0], args.rotors)

    if any(components) and not all(components):
        print("Must supply --model, --rotors, --reflector!")
        exit(-1)
    elif all(components):
        enigma_api = EnigmaAPI(*components)

    if not args.message:
        print("Supply message with --message MESSAGE argument!")
        exit(-1)

    if args.positions is not None:
        enigma_api.positions(args.positions)
    if args.ring_settings is not None:
        enigma_api.ring_settings(map(int, args.ring_settings))
    if args.plug_pairs is not None:
        enigma_api.plug_pairs(args.plug_pairs)
    if args.reflector_position is not None:
        enigma_api.reflector_position(int(args.reflector_position[0]))
    if args.reflector_pairs is not None:
        enigma_api.reflector_pairs(args.reflector_pairs)
    if args.uhr is not None:
        enigma_api.uhr(True)
        enigma_api._enigma.uhr_position(int(args.uhr[0]))

    print(enigma_api)
    print("Encrypted message:")

    for letter in args.message[0].upper():
        print(enigma_api.encrypt(letter), end='')

    print()

