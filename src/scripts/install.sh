#!/bin/bash
set -e
set -x

# upgrade
pip3 install --upgrade pip setuptools wheel

# install requirements
pip3 install -r requirements.txt