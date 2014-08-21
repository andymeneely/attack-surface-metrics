#!/bin/bash
cd $1
cflow -b `find -name "*.c"` # -o -name "*.h"
