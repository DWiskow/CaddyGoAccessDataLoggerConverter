#!/bin/sh

echo "Ready"
while true
do 
    echo "Convert logs..."
    python ./caddyLog.py -i ./input-logs/access.log -g ./output-logs/access.log
    echo "Generate report..."
    goaccess --config-file=./goaccess.conf
    echo "Report genrated."
    sleep 600
done
echo "Exited."