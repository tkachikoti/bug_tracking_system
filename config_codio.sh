#!/bin/bash

sudo apt-get update
echo | sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install --upgrade Flask
pip install -U Flask-WTF
pip install --upgrade Flask-WTF
pip install pytest
pip install --upgrade pytest
python app.py