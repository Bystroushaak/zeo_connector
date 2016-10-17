#! /usr/bin/env sh
export PYTHONPATH="src:$PYTHONPATH"

python -m pytest tests $@