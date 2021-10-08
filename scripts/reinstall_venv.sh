#!/usr/bin/bash

# This script deletes venv and reinstalls the packages in requirements.txt
rm -rf venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt --proxy proxy.esl.cisco.com