#!/bin/bash

while true; do
  /app/fliclib-linux-hci-master/bin/$ARCH/flicd -f $1 >>/var/log/flicd.out 2>&1
  echo RESTART >> /var/log/flicd.out
  wait
done