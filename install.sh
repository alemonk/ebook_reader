#!/bin/bash

sudo apt update
sudo apt upgrade

python3 -m venv pyenv
source pyenv/bin/activate

pip install pillow
pip install spidev
pip install RPi.GPIO
pip install gpiozero
pip install numpy
sudo apt-get install python3-pil

deactivate
