#!/bin/bash
export FLASK_APP=app
export FLASK_ENV=development
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app
