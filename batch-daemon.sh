#!/bin/bash

while true; do
  LOG_LEVEL=DEBUG python batch.py >> /var/log/log.out 2>&1
  echo RESTART >> /var/log/log.out
  wait
done
