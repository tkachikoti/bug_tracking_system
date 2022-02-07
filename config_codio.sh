#!/bin/bash

sudo apt-get update
echo | sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -U flask
pip install -U Flask-WTF
pip install -U pytest
python app.py