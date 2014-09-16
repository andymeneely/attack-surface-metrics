#!/bin/bash
cd "$1"
cflow -b -r `find -name "*.c"` # -o -name "*.h"
