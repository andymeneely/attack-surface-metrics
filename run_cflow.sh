#!/bin/bash
cd $1
cflow `find -name "*.c"` #  -o -name "*.h"
