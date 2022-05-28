#!/bin/bash

while true; do
  LOG_LEVEL=DEBUG CONFIG=/home/ubuntu/smart-home/config.json python smart_home.py >> ~/.smart_home.out 2>&1
  echo RESTART >> ~/.smart_home.out
  wait
done
