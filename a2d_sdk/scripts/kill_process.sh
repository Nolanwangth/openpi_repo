#!/bin/bash

# argv[1] is the process name
if [ -z "$1" ]; then
    echo "Usage: $0 <process_name>"
    exit 1
fi

ps aux | grep $1 | grep -v grep | awk '{print $2}' | xargs kill -9