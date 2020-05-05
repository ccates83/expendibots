#!/bin/bash
echo 'Running 1000 trials'

for i in {1..10000}; do python3 -m referee frostbyte random_bot; done

python3 record_parser.py
