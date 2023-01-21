# Dyson to Prometheus

This tool collects sensor data from Dyson fans and exposes these metrics to get scraped by a Prometheus server.

This is a work in progress and inspired by [https://github.com/williampiv/dyson-graph](Dyson Graph) using [https://github.com/shenxn/libdyson](Dyson Python Library) and [https://github.com/prometheus/client_python](Prometheus Python Client).

## Requirements

You will need the following information of your device(s):
- IP adress of device
- Dyson device wifi information from the sticker on the users manual or the device itself

## Setup

Get source code and create virtual environment
```
git clone https://github.com/lilaEnte/dyson-to-prom.git
cd libdyson/
python3 -m venv .venv
```

Activate environment and install required libraries
```
source .venv/bin/activate
pip3 install -r requirements.txt
```

Deactivate environment
```
deactivate
```

Start by getting the needed credentials for your device
```
.venv/bin/python3 dyson_to_prom.py -mode gen_device
```

Copy the output into a file called devices.ini (see example.devices.ini)

## Usage
```text
usage: dyson_to_prom.py [-h] [-mode {gen_device,expose,show}] [-dev [DEV]] [-port [PORT]]

Track data from Dyson fans to Prometheus

optional arguments:
  -h, --help            show this help message and exit
  -mode {gen_device,expose,show}
                        Mode: Generate information for devices.ini, expose metrics via http to get scraped by prometheus or print to command line.
  -dev [DEV]            Devices file: /path/to/devices.ini.
  -port [PORT]          Set Port to serve metrics on. Defaults to 8000.
```

## Setup as a service through systemctl/systemd

Create service config file
```
sudo nano /etc/systemd/system/dyson-metrics.service
```

Fill with following content (adjust paths to your needs)
```ini
[Unit]
Description=Serve dyson metrics as http service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
Restart=always
ExecStart=/path/to/your/dyson-to-prom/.venv/bin/python3 /path/to/your/dyson-to-prom/dyson_to_prom.py -mode expose -dev /path/to/your/dyson-to-prom/devices.ini

[Install]
WantedBy=multi-user.target
```

Reload config, enable and startup service
```
sudo systemctl daemon-reload
sudo systemctl enable dyson-metrics.service
sudo systemctl start dyson-metrics.service
```

Server should now be running on [http://localhost:8000/](http://localhost:8000/)
If you want to change the port have a look at the `-port` parameter under [https://github.com/lilaEnte/dyson-to-prom#usage](Usage)

## Setup Prometheus to scrape data

Edit prometheus config file
```
sudo nano /etc/prometheus/prometheus.yml
```

Add the following job to `scrape_configs:` section
```
  - job_name: 'dyson'

    scrape_interval: 60s

    static_configs:
      - targets: [localhost:8000]

```

Restart Prometheus
```
sudo systemctl restart prometheus
```
