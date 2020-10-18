# vehicle client

Client reads GPS coords and sends them to the server.

## Installation

(For Raspberry PI)

```bash
wget https://raw.githubusercontent.com/odwyersoftware/vehicle-gps-tracker/master/client/install.sh
sh install.sh

# Make it run on boot
crontab -e
# Add this line to the file to
@reboot sleep 60 && /home/pi/startup_tracker.sh
# reboot
```

Other systems

```bash
sudo apt-get install gpsd gpsd-clients
pip install -r requirements-dev.txt
```

## Usage

(For Raspberry PI)

```bash
wget https://raw.githubusercontent.com/odwyersoftware/vehicle-gps-tracker/master/client/run.sh
export SERVER_WRITE_ENDPOINT=http://localhost:8080/write
sh run.sh
```

Other systems

```bash
export SERVER_WRITE_ENDPOINT=http://localhost:8080/_write
python main.py
```
