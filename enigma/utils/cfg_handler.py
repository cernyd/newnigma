#!/usr/bin/env python3

import json


class Config:
    def __init__(self, path):
        """
        :param path: {str} path to .json config file
        """
        self.__path = path

    def mk_cache(self):
        """
        Loads config file and caches it to self.cache
        """
        self.cache = self.load()

    def load(self):
        """
        Loads configuration and returns deserialized json as a dictionary
        :returns: {dict} deserialized config data
        """
        try:
            with open(self.__path, 'r') as config:
                return json.loads(config.read())
        except FileNotFoundError:
            print("Config file not found!")

    def save(self, data):
        """
        Writes serialized json data to config path
        :param data: {dict} data to write to config
        """
        with open(self.__path, 'w') as config:
            json.dump(data, config, indent=4)
