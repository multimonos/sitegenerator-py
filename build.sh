#!/usr/bin/env bash

clear
python src/main.py
cat ./public/index.html | tidy -i
