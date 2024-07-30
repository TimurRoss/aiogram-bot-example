#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
PORT=$1
source $BASEDIR/env/bin/activate
python $BASEDIR/main.py $PORT
