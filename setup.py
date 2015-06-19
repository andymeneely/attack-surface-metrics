try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

setup(
    name='attacksurfacemeter',
    version='0.9.0',
    packages=[
        'attacksurfacemeter',
        'attacksurfacemeter.loaders',
        'attacksurfacemeter.formatters'
    ],
    package_data={
        'attacksurfacemeter': [
            'data/android_edge_black_list',
            'data/android_input_methods',
            'data/android_output_methods',
            'data/android_override_input_methods',
            'data/android_override_output_methods',
            'data/android_package_black_list',
            'data/c_std_lib_functions',
            'data/c_input_functions',
            'data/c_output_functions'
        ],
        'attacksurfacemeter.loaders': [
            'run_cflow.sh',
            'run_cflow_r.sh'
        ],
        'attacksurfacemeter.formatters': [
            'database.create.pgsql.sql',
            'database.create.sqlite.sql',
            'summary_template.html',
            'summary_template.txt',
            'template.html',
            'template.txt',
        ],
    },
    install_requires=['networkx==1.9.1', 'django==1.7.4'],
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
