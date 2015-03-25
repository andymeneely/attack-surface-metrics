#!/bin/bash
cd "$1"
cflow -b -r `find -name '*.c' -or -name '*.h' | grep -vwE '(tests|doc)'`