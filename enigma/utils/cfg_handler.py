#!/usr/bin/env python3
"""Functions for loading from and saving to JSON files."""

import json
import logging


def load_config(filename):
    """Attempts to load JSON serialized data from a file
    :param filename: {str} Path to config file
    """
    logging.info('Attempting to load from file "%s"...', filename)
    try:
        with open(filename, "r") as config:
            return json.loads(config.read())
    except FileNotFoundError:
        logging.error('Config file "%s" not found!', filename, exc_info=True)
        raise
    except json.JSONDecodeError:
        logging.error(
            'Decoding error, file "%s" possibly corrupted.', filename, exc_info=True
        )
        raise


def save_config(filename, data):
    """Attempts to save JSON serialized data to a file
    :param filename: {str} Path to config file
    :param data: {dict} Dictionary of dumped config
    """
    logging.info('Saving config to file "%s"...', filename)
    with open(filename, "w") as config:
        json.dump(data, config, indent=4)
