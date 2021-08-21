#!/bin/bash
set -e
set -x

# run python install script
python3 install.py

# run camunda
# ./bpm_run/start.sh