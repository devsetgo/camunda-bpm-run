#!/bin/bash
set -e
set -x

# run camunda
./bpm_run/start.sh
# ./bpm_run/start.sh --production --webapps --rest