#!/bin/bash
cd "$1"
cflow -b `find -name '*.c' -or -name '*.h' | grep -vwE '(tests|doc)'`
