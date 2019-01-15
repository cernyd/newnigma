import argparse
from enigma.api.enigma_api import EnigmaAPI
import logging


def cli(default_api, args):
    logging.info('Launching newnigma in the command line...')

    enigma_api = default_api

    components = (args.model, args.rotors, args.reflector)
    if any(components) and not all(components):
        print("Must supply --model, --rotors, --reflector!")
        exit(-1)
    elif all(components):
        model = args.model[0]
        rotors = args.rotors
        reflector = args.reflector[0]

        # Override default enigma api
        enigma_api = EnigmaAPI(model, reflector, rotors)

    if not args.message:
        print("Supply message with --message MESSAGE argument!")
        exit(-1)

    if args.positions is not None:  # TODO: Implement into EnigmaAPI
        enigma_api.positions(args.positions)
    if args.ring_settings is not None:
        enigma_api.ring_settings(map(int, args.ring_settings))
    if args.plug_pairs is not None:
        enigma_api.plug_pairs(args.plug_pairs)

    print(enigma_api)
    print("Encrypted message:")

    for letter in args.message[0].upper():
        print(enigma_api.encrypt(letter), end='')

    print()
    


def preview(self):
    print("Copy the command below:\n\n./newnigma.py --cli --model Enigma1 --rotors II I III " \
          "--reflector UKW-A --message THISISANENIGMASAMPLEMESSAGE")
    exit()
