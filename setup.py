try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(
    name='attacksurfacemeter',
    version='0.4.0',
    packages=[
        'attacksurfacemeter',
        'attacksurfacemeter.loaders',
        'attacksurfacemeter.formatters',
    ],
    install_requires=['networkx==1.9.1','django==1.6'],
    license='The MIT License (MIT) Copyright (c) 2015 Andy Meneely',
    description='Library for collecting metrics of the attack surface.',
    long_description=open('README.md').read(),
    author='Andy Meneely',
    author_email='andy@se.rit.edu',
    url='https://github.com/andymeneely/attack-surface-metrics',
    test_suite="tests",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
    ],
)
