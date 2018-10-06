#!/usr/bin/env python3
"""
Copyright (C) 2016, 2017  David Cerny

This file is part of gnunigma

Gnunigma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from collections import OrderedDict
from os import path
import yaml


def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    """Loads data while keeping data order"""
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    return yaml.load(stream, OrderedLoader)


class Config:
    """YAML configuration parser and manager"""
    def __init__(self, buffer_path, load_type='ordered'):
        if type(buffer_path) == str:
            self.buffer_path = buffer_path
        else:
            self.buffer_path = path.join(*buffer_path)
        with open(self.buffer_path, 'r') as file:
            if load_type == 'ordered':
                self.data = ordered_load(file)
            elif load_type == 'unordered':
                self.data = yaml.safe_load(file)

    def write(self):
        """Writes changes to the config file."""
        with open(self.buffer_path, 'w') as file:
            yaml.safe_dump(self.data, file)
