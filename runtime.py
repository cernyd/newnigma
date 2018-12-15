#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Returns Enigma encrypted text base on settings and provided text.")
parser.add_argument('--test', help="Runs tests before launching the program to ensure it works correctly.",
                    action="store_true", default=False, dest="run_tests")

import sys
from PyQt5 import QtGui, QtWidgets


if __name__ == '__main__':

    result = parser.parse_args()
    if result.run_tests:
        print("RUN TESTS HERE")
