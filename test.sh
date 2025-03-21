#!/usr/bin/env bash

# python -m unittest discover -s src
#
ls ./src/*.py |entr -c pytest --tb=short ./src/*.py
