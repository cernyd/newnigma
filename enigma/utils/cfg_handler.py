#!/usr/bin/env python3

import json
import logging


def load_config(path):
    logging.info('Attempting to load from file "%s"...' % path)
    try:
        with open(path, "r") as config:
            return json.loads(config.read())
    except FileNotFoundError:
        logging.error('Config file "%s" not found!' % path, exc_info=True)
        raise
    except json.JSONDecodeError:
        logging.error('Decoding error, file "%s" possibly corrupted.' % path, exc_info=True)
        raise


def save_config(path, data):
    logging.info('Saving config to file "%s"...' % path)
    with open(path, "w") as config:
        json.dump(data, config, indent=4)
