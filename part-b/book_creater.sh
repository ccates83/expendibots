#!/bin/bash
echo 'Running 1000 trials'

for i in {1..1000}; do python3 -m referee random_bot random_bot; done

python3 record_parser.py
