#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Cygni_Python_Snakeclient',
    version='0.1',
    description="Client for Cygni's snakebot competition",
    author='Martin Barksten',
    author_email='martin.barksten@cygni.se',
    url='http://game.snake.cygni.se',
    packages=['client'],
    install_requires=['gym', 'numpy', 'pygame']
    )

