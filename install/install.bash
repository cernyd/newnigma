#! /bin/bash
sudo apt update
sudo apt install -y python3-pip pytest
sudo -H pip3 install --upgrade pip
sudo -H pip3 install -r requirements.txt
