#!/bin/sh
# Activate Virtual Environment
source /home/kevin/virtualenvs/attack-surface-metrics/bin/activate

# Deactivate Virtual Environment
deactivate

# Package Release and upload
python setup.py sdist upload

