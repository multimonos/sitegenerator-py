#!/usr/bin/env bash

clear

python src/main.py

# show html
if [ "$1" = "-v" ]; then
  cat ./public/index.html | tidy -i -w 120
fi
