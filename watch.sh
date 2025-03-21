#!/usr/bin/env bash
clear
#ls ./src/*.py |entr -c pytest -s --tb=short ./src/*.py
ls ./src/*.py |entr -c pytest -s ./src/*.py
