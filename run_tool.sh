#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "Error: Python3 is not installed. Please install it to continue."
    exit 1
fi

python3 main.py