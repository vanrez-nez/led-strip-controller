# Getting started with the project

## Prerequisites
- Python 3.10 or higher
- pip
- venv

## Installation
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install the dependencies: `pip install -r requirements.txt`
5. Run the project: `python main.py`

## On the Raspberry Pi
1. Once inside the virtual environment you'll need to install the GPIO library: `pip install RPi.GPIO` and `pip install rpi_ws281x`
2. Because the GPIO library requires root access, you'll need to run the script with `sudo` (before activating your virtual env): `sudo ./venv/bin/python src/visualizer.py`

3. UART comms with ESP32 `pip3 install pyseria`

## Admin Visualizer Service
Setup and admin the service by:
`sudo nano /etc/systemd/system/led-visualizer.service`
With contents:
```
[Unit]
Description=LED Strip Controller Visualizer
After=network.target

[Service]
WorkingDirectory=/home/pi/led-strip-controller
ExecStart=/home/pi/led-strip-controller/venv/bin/python /home/pi/led-strip-controller/src/visualizer.py
# No User/Group lines here means it runs as root by default
Restart=always

[Install]
WantedBy=multi-user.target
```
then:
`sudo systemctl daemon-reload`
`sudo systemctl enable led-visualizer.service`

Admin service status using commands:
`sudo systemctl restart led-visualizer.service`
`sudo systemctl stop led-visualizer.service`
`sudo systemctl start led-visualizer.service`