#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import yaml


parser = ArgumentParser(description='An emulator of the Enigma encryption machine.')
parser.add_argument('--test', const=True, nargs='?',
                    help='run integrated tests to validate correct functionality')

print(vars(parser.parse_args()))

if __name__ == '__main__':
    print("Program run")
    with open('data/config.yaml', 'r') as file:
        print(yaml.load(file))
