import configparser as c
import sys
import time
import argparse
import re

from libdyson import get_mqtt_info_from_wifi_info
from libdyson.exceptions import DysonFailedToParseWifiInfo

from prometheus_client import start_http_server
from model.dyson_device import DysonDevice
from model.prom_metric import PromMetric


if __name__ == "__main__":
    # read in the parser items
    parser = argparse.ArgumentParser(description="Track data from Dyson fans to Prometheus")
    parser.add_argument(
        "-mode",
        choices=["gen_device", "expose", "show"],
        help="Mode: Generate information for devices.ini, expose metrics via http to get scraped by prometheus or print to command line.",
    )
    parser.add_argument("-dev", nargs='?', help="Devices file: /path/to/devices.ini.")
    parser.add_argument("-port", nargs='?', const=8000, type=int, help="Set Port to serve metrics on. Defaults to 8000.")
    args = parser.parse_args()
    
    
    
    if args.mode == "gen_device":
        print("This will generate the information for one device which needs to be copied into devices.ini.")
        
        location = input("Device location or room: ")
        ip = input("Device IP: ")
        wifi_ssid = input("Device wifi SSID: ")
        wifi_password = input("Device wifi password: ")

        location = re.sub(r"[^a-zA-Z0-9]", '_', location)

        try:
            serial, credential, device_type = get_mqtt_info_from_wifi_info(
                wifi_ssid, wifi_password
            )
        except DysonFailedToParseWifiInfo:
            print("Failed to parse SSID.")
        
        print()
        print("[" + location + "]")
        print("ip_address =", ip)
        print("username =", serial)
        print("password =", credential)
        print("dev_type =", device_type)
        print()
    
    else:
        # read configured dyson devices
        dyson_devices = c.ConfigParser()

        try:
            dyson_devices.read(args.dev)
        except Exception as e:
            print(e)
            sys.exit(1)
        
        devices = {}
        readings = {}
        prom = {}
            
        for section in dyson_devices.sections():
            devices[section] = DysonDevice(dyson_devices[section]["ip_address"], dyson_devices[section]["username"], dyson_devices[section]["password"], dyson_devices[section]["dev_type"])
            readings[section] = devices[section].get_dyson_readings()
            
            prom[section] = PromMetric(section, "dyson_" + dyson_devices[section]["dev_type"])
            prom[section].generate_metrics(readings[section])
            
            
        if args.mode == "expose":
        
            if args.port:
                port = args.port
            else:
                port = 8000
     
            try:
                start_http_server(port)          
            except Exception as e:
                print("Failed to start server at port " + port + ".")
                print(e)
                sys.exit(1)
            
            while True:
                for section in dyson_devices.sections():
                    readings[section] = devices[section].get_dyson_readings()
                    
                    prom[section].update_metrics(readings[section])
                    print(section,":",readings[section])
                
                time.sleep(60)
                    
        elif args.mode == "show":
            for section in dyson_devices.sections():
                devices[section].info(section)

