from typing import Dict

import prometheus_client
from prometheus_client import Gauge

class PromMetric:
    metrics = {}
    location = ""
    type = ""

    def __init__(self, loc, t):
        self.location = loc
        self.type = t
        
        # Disable Default Collector metrics
        prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
        prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

    def generate_metrics(self, readings: Dict):
        for key in readings.keys():
            g = Gauge(key, "", labelnames=["location", "collection"])
            g.labels(self.location, self.type).set(readings[key])
            self.metrics[key] = g

    def update_metrics(self, readings: Dict):
        for key in readings.keys():
            self.metrics[key].labels(self.location, self.type).set(readings[key])