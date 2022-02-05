#!/bin/bash

sudo apt-get update
echo | sudo apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install pytest
python app.py