#!/bin/bash

sudo apt-get install python3-tk
sudo apt-get install python3-pip
python -m pip3 install pipenv

python -m pipenv install
python -m pipenv run python -m colorization_program
