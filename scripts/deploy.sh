#!/usr/bin/bash

# This script copies everything from the current directory (except venv and requirements.txt) to the ubuntu server into
# the ~/Documents/BAT_RAT directory
echo "Copying everything except venv/ and requirements.txt from $(pwd) to rattool@10.52.247.154:~/Documents/BAT_RAT/"
scp -r ./[!venv][!requirements.txt]* rattool@10.52.247.154:~/Documents/BAT_RAT/

