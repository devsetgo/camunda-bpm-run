#!/bin/bash
set -e
set -x

# upgrade
docker build -t mikeryan56/bpm:7.14-b7 .

# run
# docker run mikeryan56/bpm:7.14-b6