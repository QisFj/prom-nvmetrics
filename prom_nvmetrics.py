from prometheus_client import start_http_server, Summary, Gauge
import sys
import time
import xml.etree.ElementTree as ET
import py3nvml.nvidia_smi as smi

# initialize GPUs to get dynamic name assignment for metric description
def initialize_gpus():
    smi.nvmlInit()
    print("Driver Version: ", smi.nvmlSystemGetDriverVersion())
    out = smi.XmlDeviceQuery()
    root = ET.fromstring(out)
    atleastOne = False
    for gpu in root.iter("gpu"):
        name = gpu.find("product_name").text
        pciBus = gpu.find("pci").find("pci_bus").text
        print("Found: " + name + " -- " + pciBus)
        atleastOne = True
    if not atleastOne:
        raise "Not Found Any GPU"

    labelnames = ["card", "pci_bus"]

    return {
        "gTemperature": Gauge("GPU_Temperature", "Temperature of GPU", labelnames=labelnames),
        "gfan_speed": Gauge("GPU_fan_speed", "Fan Speed of GPU", labelnames=labelnames),
        "gfb_memory_usage": Gauge("GPU_memory_usage", "Memory usage of GPU", labelnames=labelnames),
        "gfb_memory_total": Gauge("GPU_memory_total", "Total Memory usage of GPU", labelnames=labelnames),
        "ggraphics_clock": Gauge("GPU_graphics_clock", "Graphics clock of GPU", labelnames=labelnames),
        "gmem_clock": Gauge("GPU_memory_clock", "Memory clock of GPU", labelnames=labelnames),
        "gpower_draw": Gauge("GPU_power_draw", "Power draw of GPU", labelnames=labelnames),
        "ggpu_util": Gauge("GPU_util", "Utilization of GPU", labelnames=labelnames),
    }

def find_float(gpu, key):
    return float(gpu.find(key).text.split()[0])

def set_metric(metric, labels: tuple, value: float):
    # print(metric._name, metric._labelnames, labels, value)
    metric.labels(*labels).set(value)

def execute_and_read_from_SMI(metrics):
    """A dummy function that takes some time."""

    gTemperature = metrics.get("gTemperature", "default")
    gfan_speed = metrics.get("gfan_speed", "default")
    gfb_memory_usage = metrics.get("gfb_memory_usage", "default")
    gfb_memory_total = metrics.get("gfb_memory_total", "default")
    ggraphics_clock = metrics.get("ggraphics_clock", "default")
    gmem_clock = metrics.get("gmem_clock", "default")
    gpower_draw = metrics.get("gpower_draw", "default")
    ggpu_util = metrics.get("ggpu_util", "default")

    out = smi.XmlDeviceQuery()
    root = ET.fromstring(out)
    # print(out)
    for gpu in root.iter("gpu"):
        labels = (gpu.find("product_name").text, gpu.find("pci/pci_bus").text)
        
        set_metric(gTemperature, labels, find_float(gpu, "temperature/gpu_temp"))
        set_metric(gfan_speed, labels, find_float(gpu, "fan_speed"))
        set_metric(gfb_memory_usage, labels, 1e6 * find_float(gpu, "fb_memory_usage/used"))
        set_metric(gfb_memory_total, labels, 1e6 * find_float(gpu, "fb_memory_usage/total"))
        set_metric(ggraphics_clock, labels, find_float(gpu, "clocks/graphics_clock"))
        set_metric(gmem_clock, labels, find_float(gpu, "clocks/mem_clock"))
        set_metric(gpower_draw, labels, find_float(gpu, "power_readings/power_draw"))
        set_metric(ggpu_util, labels, find_float(gpu, "utilization/gpu_util"))

if __name__ == "__main__":
    # initialize the metrics from GPU
    metrics = initialize_gpus()
    # Start up the server to expose the metrics.
    port = 8000 # default port 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("invalid argument: port:", port)
            sys.exit(1)
    print("Starting server on port: " + str(port))
    start_http_server(port)
    # Generate some requests.
    while True:
        # print('update metrics')
        execute_and_read_from_SMI(metrics)
        # print('sleep')
        time.sleep(5)
