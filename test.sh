#!/bin/sh

SOURCEFILE=./src/snake.py

black --check ${SOURCEFILE} && pylint ${SOURCEFILE} && echo success || ( echo FAILURE ; exit 1 )
