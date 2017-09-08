#!/usr/bin/env python

from setuptools import setup, find_packages
import os

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='storagex',
    version='0.1',
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

