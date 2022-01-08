# why fork 

- to allow multi GPUs

- adpat to winsw:

    use prom_nvmetrics.exe to run, see https://github.com/winsw/winsw/tree/master#usage for more.

    winsw binary version: [v2.11.0-x64](https://github.com/winsw/winsw/releases/download/v2.11.0/WinSW-x64.exe)

# A simple prometheus exporter for metrics of NVIDIA based GPUs
* Inofficial no affiliation with NVIDIA
* For usage in a grafana https://grafana.com/ + prometheus https://prometheus.io/ monitoring setup
* Uses py3nvml https://github.com/fbcotter/py3nvml
* Tested on windows and linux
* No multi GPUs

## Dependencies:
* python 3.x ( tested on 3.5 )
* pip install py3nvml
* pip install prometheus_client

## Supported metrics
* Temperature of GPU
* Fan Speed of GPU
* Memory usage
* Total Memory
* Graphics clock
* Memory clock
* Utilization of GPU
* Power draw

More can be added simply

## Usage
* Run python prom_nvmetrics.py
* Make sure to use your 64 bit python installation if your nvidia driver is also 64 bit
* It will listen on port 8000 per default, metrics available at http://localhost:8000/metrics
* Use your prometheus + grafana setup to add it as target and build a nice dashboard

