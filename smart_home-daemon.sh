#!/bin/bash

while true; do
  LOG_LEVEL=DEBUG CONFIG=$CONFIG python smart_home.py >> /var/log/smart_home.out 2>&1
  echo RESTART >> /var/log/smart_home.out
  wait
done
