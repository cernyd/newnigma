#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup


package_name = 'gnunigma'
filename = package_name + '.py'


def get_long_description():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except IOError:
        return ''


setup(
    name=package_name,
    version='v1.5.2',
    author='David Černý',
    author_email='cernydcer@gmail.com',
    description='Enigma encryption machine emulation in python.',
    url='https://github.com/cernyd/gnunigma',
    long_description=get_long_description(),
    py_modules=[package_name],
    license='License :: OSI Approved :: GNU GPLv3 License',
)