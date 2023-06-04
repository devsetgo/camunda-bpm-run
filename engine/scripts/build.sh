#!/bin/bash
set -e
set -x

# Build
# docker build -t mikeryan56/bpm:7.14-b7 .

CAL_VER=$(TZ=America/New_York date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t mikeryan56/bpm:7.14-$CAL_VER -f dockerfile .
docker tag mikeryan56/bpm:7.14-$CAL_VER mikeryan56/bpm:latest
docker push mikeryan56/bpm:7.14-$CAL_VER
docker push mikeryan56/bpm:latest