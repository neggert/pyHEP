#!/usr/bin/env python

from setuptools import setup

setup(name='pyHEP',
      version='0.1alpha1',
      description='Python for High Energy Physics',
      author='Nic Eggert',
      author_email='nse23@cornell.edu',
      install_requires=['ZODB3'],
      packages=['pyhep']
      )
