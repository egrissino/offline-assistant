#!/bin/bash
now=`date`
echo $now
cd /home/admin/workspace/offline-assistant
./bin/python3 ./offline-speech.py --serve-in-foreground > "./logs/${now}_assistant.log"
