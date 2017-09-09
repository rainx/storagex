#!/usr/bin/env python

from setuptools import setup, find_packages
import os

long_description = 'a library to storage file to cyber space'


setup(
    name='storagex',
    version='0.2',
    description='just storagex',
    long_description=long_description,
    author='RainX<Jing Xu>',
    author_email='i@rainx.cc',
    url='https://github.com/rainx/storagex',
    packages=find_packages(),
    install_requires=[
            'click',
            'six',
            'requests',
            'cryptography',
            'Pillow'
    ],
    entry_points={
          'console_scripts': [
              'storagex=storagex.commandline:storagex'
          ]
      },
    )

