__author__ = 'kevin'

from distutils.core import setup

setup(
    name='AttackSurfaceMeter',
    version='0.0.1',
    packages=['attack_surface',],
    requires=['networkx', 'matplotlib'],
    license='The MIT License (MIT) Copyright (c) 2014 Andy Meneely',
    long_description=open('README.md').read(),
    author='Kevin Campusano',
    author_email='kac2375@rit.edu',
    url='https://github.com/andymeneely/attack-surface-metrics'
)