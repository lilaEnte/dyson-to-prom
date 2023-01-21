import libdyson as ld

from libdyson import DEVICE_TYPE_NAMES
from libdyson.const import (
    DEVICE_TYPE_PURE_COOL,
    DEVICE_TYPE_PURE_COOL_DESK,
    DEVICE_TYPE_PURE_COOL_FORMALDEHYDE,    
    DEVICE_TYPE_PURE_COOL_LINK,
    DEVICE_TYPE_PURE_COOL_LINK_DESK,
)

class DysonDevice:

    ip = ""
    username = ""
    password = ""
    type = ""

    def __init__(self, ip: str, u: str, p: str, t: str):
        self.ip = ip
        self.username = u
        self.password = p
        self.type = t
        
    def kelvin_to_celsius(self, kelvin_temp: float) -> float:
        return round((kelvin_temp - 273.15), 2)

    def get_dyson_readings(self) -> dict:
        device = ld.get_device(self.username, self.password, self.type)
        device.connect(self.ip)
           
        readings = {
            "temperature": self.kelvin_to_celsius(device.temperature),
            "humidity": device.humidity,    
        }
        
        if self.type in [
            DEVICE_TYPE_PURE_COOL,
            DEVICE_TYPE_PURE_COOL_DESK,
            DEVICE_TYPE_PURE_COOL_FORMALDEHYDE,
        ]:  
            readings["particulate_matter_2_5"] =  device.particulate_matter_2_5
            readings["particulate_matter_10"] =  device.particulate_matter_10
            readings["volatile_organic_compounds"] =  device.volatile_organic_compounds
            readings["nitrogen_dioxide"] =  device.nitrogen_dioxide
            readings["filter_life_hepa"] =  device.hepa_filter_life
            readings["filter_life_carbon"] =  device.carbon_filter_life
        
        if self.type in [
            DEVICE_TYPE_PURE_COOL_LINK,
            DEVICE_TYPE_PURE_COOL_LINK_DESK,
        ]:
            readings["filter_life"] = device.filter_life
            readings["dyson_particulates"] = device.particulates
            readings["dyson_volatile_organic_compounds"] = device.volatile_organic_compounds

        
        device.disconnect()
        return readings

    def info(self, section: str):
        device = ld.get_device(self.username, self.password, self.type)
        device.connect(self.ip)
        
        print()
        print("Device Location:", section)
        print("Device Type:", self.type)
        print("Device Type Name:", DEVICE_TYPE_NAMES[self.type])
        
        if self.type in [
            DEVICE_TYPE_PURE_COOL,
            DEVICE_TYPE_PURE_COOL_DESK,
            DEVICE_TYPE_PURE_COOL_FORMALDEHYDE,
            DEVICE_TYPE_PURE_COOL_LINK_DESK,
            DEVICE_TYPE_PURE_COOL_LINK,
        ]:
            print()
            print("[Exposable Metrics]")
            print("Temp (°C):\t\t\t", self.kelvin_to_celsius(device.temperature), "\t(metric name: temperature)")
            print("Humidity (%):\t\t\t", device.humidity, "\t(metric name: humidity)")      
            #print("Fan State:", device.fan_state)
            #print("Fan Speed:", device.speed)
 
            if self.type in [
                DEVICE_TYPE_PURE_COOL,
                DEVICE_TYPE_PURE_COOL_DESK,
                DEVICE_TYPE_PURE_COOL_FORMALDEHYDE,
            ]:  
                print("Particulate Matter 2.5 (µg/m³):\t", device.particulate_matter_2_5, "\t(metric name: particulate_matter_2_5)")
                print("Particulate Matter 10 (µg/m³):\t", device.particulate_matter_10, "\t(metric name: particulate_matter_10)")
                print("VOCs (µg/m³):\t\t\t", device.volatile_organic_compounds, "\t(metric name: volatile_organic_compounds)")
                print("Nitrogen Dioxide (µg/m³):\t", device.nitrogen_dioxide, "\t(metric name: nitrogen_dioxide)")
                print("Hepa Filter Life (%):\t\t", device.hepa_filter_life, "\t(metric name: filter_life_hepa)")
                print("Carbon Filter Life (%):\t\t", device.carbon_filter_life, "\t(metric name: filter_life_carbon)")
                
            if self.type in [
                DEVICE_TYPE_PURE_COOL_LINK,
                DEVICE_TYPE_PURE_COOL_LINK_DESK,
            ]:  
                print("Filter life (hour):\t\t", device.filter_life, "\t(metric name: filter_life)") 
                print("Particulates (unknown unit):\t", device.particulates, "\t(metric name: dyson_particulates)")
                print("VOCs (unknown unit):\t\t", device.volatile_organic_compounds, "\t(metric name: dyson_volatile_organic_compounds)")
        else:
            print()
            print("This device type is currently not supported by this application.")
        
        
        device.disconnect()

        