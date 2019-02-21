#!/usr/bin/env python3

import json


def load_config(path):
    try:
        with open(path, "r") as config:
            return json.loads(config.read())
    except FileNotFoundError:
        print("Config file not found!")


def save_config(path, data):
    with open(path, "w") as config:
        json.dump(data, config, indent=4)
