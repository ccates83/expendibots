#!/bin/bash
echo 'Running 1000 trials'

for i in {1..1000}; do
  echo $i;
  python3 -m referee frostbyte random_bot > out.txt;
done

python3 record_parser.py
