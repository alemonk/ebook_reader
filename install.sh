#!/bin/bash

# sudo apt update
# sudo apt upgrade

sudo apt install python3-pip
sudo apt-get install python3-venv
python3 -m venv pyenv
source pyenv/bin/activate

pip install pillow
pip install spidev
pip install RPi.GPIO
pip install gpiozero
pip install numpy
sudo apt-get install python3-pil
pip install ebooklib
pip install bs4
pip install lgpio
pip install quotes-library

deactivate
