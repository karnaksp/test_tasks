#!/bin/bash
apt-get -y update
apt-get install -y poppler-utils
apt-get install -y ufw python3-apt libcairo2-dev libgirepository1.0-dev libsystemd-dev
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt --no-cache-dir
python3 -m pip install tools
python3 api.py
