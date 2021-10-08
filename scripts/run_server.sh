#!/usr/bin/bash

source venv/bin/activate
nohup python app.py > logs/log.txt 2>&1
