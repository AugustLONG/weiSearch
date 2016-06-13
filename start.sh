#!/bin/bash

service mongod start &

cd bin
python control.py main.py start &

cd ../flask
python app.py