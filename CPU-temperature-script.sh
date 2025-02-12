#!/bin/bash

TEMPERATURE=$(sensors | grep "Core 0" | cut -d + -f 2 | cut -d . -f1)

if [ $TEMPERATURE -ge 45 ]; then
	date=$(date '+%Y-%m-%d %H:%M:%S')
	echo "$date HIGH_temperature: $TEMPERATURE"  >> /data/logs/cpu_temp.log
fi
