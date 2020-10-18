#!/usr/bin/env sh
set -e
sudo apt-get install gpsd gpsd-clients
sudo systemctl enable ssh
sudo systemctl start ssh
git clone --depth 1 https://github.com/odwyersoftware/tracker ~/tracker
