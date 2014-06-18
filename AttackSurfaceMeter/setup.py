__author__ = 'kevin'

from distutils.core import setup

setup(
    name='AttackSurfaceMeter',
    description='Library for collecting metrics of the attack surface.',
    version='0.0.1',
    packages=['attacksurfacemeter',],
    requires=['networkx', 'matplotlib'],
    license='The MIT License (MIT) Copyright (c) 2014 Andy Meneely',
    description='Scripts for collecting metrics of the attack surface',
    long_description=open('README.md').read(),
    author='Kevin Campusano',
    author_email='kac2375@rit.edu',
    url='https://github.com/andymeneely/attack-surface-metrics'
)
