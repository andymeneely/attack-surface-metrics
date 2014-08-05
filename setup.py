__author__ = 'kevin'

# from distutils.core import setup
from setuptools import setup

setup(
    name='AttackSurfaceMeter',
    version='0.0.2',
    packages=['attacksurfacemeter', 'formatters'],
    requires=['networkx', 'matplotlib'],
    license='The MIT License (MIT) Copyright (c) 2014 Andy Meneely',
    description='Library for collecting metrics of the attack surface.',
    long_description=open('README.md').read(),
    author='Kevin Campusano',
    author_email='kac2375@rit.edu',
    url='https://github.com/andymeneely/attack-surface-metrics',
    test_suite="tests"
)
