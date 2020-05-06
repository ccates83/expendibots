#!/bin/bash
echo 'Running 1000 trials, keeping track of winners'

for i in {1..1000}; do
  echo $i;
  python3 -m referee frostbyte random_bot > out.txt;
done

python3 score_parser.py
