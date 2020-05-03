#!/usr/bin/env bash

python3 -m venv env
source ./env/bin/activate
pip3 install --upgrade pip --user
pip3 install --requirement requirements.txt