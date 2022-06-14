#!/bin/bash

while true; do
  LOG_LEVEL=DEBUG python batch.py >> /var/log/batch.out 2>&1
  echo RESTART >> /var/log/batch.out
  wait
done
