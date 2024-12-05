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
1. Once inside the virtual environment you'll need to install the GPIO library: `pip install RPi.GPIO`
2. Because the GPIO library requires root access, you'll need to run the script with `sudo` (before activating your virtual env): `sudo ./venv/bin/python src/visualizer.py`