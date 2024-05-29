import time
import random
from os import path
import yaml
from prometheus_client.core import (
    GaugeMetricFamily,
    REGISTRY,
    CounterMetricFamily,
    StateSetMetricFamily,
)
from prometheus_client import start_http_server
from vartastorage.vartastorage import VartaStorage

totalRandomNumber = 0


class VartaCollector(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

        pass

    def collect(self):
        varta = VartaStorage(self.host, self.port)
        # read all data from Varta Storage
        varta.get_all_data_modbus()
        varta.get_energy_cgi()
        
        # Create metrics
        installed_capacity = GaugeMetricFamily(
            "varta_installed_capacity",
            "installed capacity in Wh",
        )
        installed_capacity.add_metric(
            ["varta_installed_capacity"], str(varta.installed_capacity)
        )
        yield installed_capacity

        state_of_charge = GaugeMetricFamily(
            "varta_state_of_charge",
            "total state of charge in %",
        )
        state_of_charge.add_metric(["installed_capacity"], str(varta.soc))
        yield state_of_charge
        
        total_charged_energy = GaugeMetricFamily(
            "varta_total_charged_energy",
            "total charged energy in kWh",
        )
        total_charged_energy.add_metric(["varta_installed_capacity"], str(varta.soc))
        yield total_charged_energy
        
        from_grid_power = GaugeMetricFamily(
            "varta_from_grid_power",
            "energy from grid to home in W",
        )
        from_grid_power.add_metric(["varta_installed_capacity"], str(varta.from_grid_power))
        yield from_grid_power
        
        
        to_grid_power = GaugeMetricFamily(
            "varta_to_grid_power",
            "energy from home to grid in W",
        )
        to_grid_power.add_metric(["varta_installed_capacity"], str(varta.to_grid_power))
        yield to_grid_power
        

        charge_cycle_counter = CounterMetricFamily(
            "varta_charge_cycle_counter",
            "charge load cycles from",
        )
        charge_cycle_counter.add_metric(
            ["varta_installed_capacity"], str(varta.charge_cycle_counter)
        )
        yield charge_cycle_counter

        state = StateSetMetricFamily(
            "varta_bat_state",
            "state of system: BUSY, RUN, CHARGE, DISCHARGE, STANDBY, ERROR, PASSIVE, ISLANDING",
        )
        allBatStates = {}
        allBatStates["BUSY"] = False
        allBatStates["RUN"] = False
        allBatStates["CHARGE"] = False
        allBatStates["DISCHARGE"] = False
        allBatStates["STANDBY"] = False
        allBatStates["ERROR"] = False
        allBatStates["PASSIVE"] = False
        allBatStates["ISLANDING"] = False
        allBatStates[varta.state_text] = True
        state.add_metric(["state"], allBatStates)
        yield state


if __name__ == "__main__":
    port = 3000
    frequency = 1
    varta_host = "localhost"
    varta_port = 502
    # TODO correccting error handling
    if path.exists("/etc/varta/config.yml"):
        with open("/etc/varta/config.yml", "r") as config_file:
            try:
                config = yaml.safe_load(config_file)
                port = int(config["port"])
                frequency = config["scrape_frequency"]
                varta_host = config["varta_host"]
                varta_port = int(config["varta_port"])
            except yaml.YAMLError as error:
                print(error)
    start_http_server(port)
    REGISTRY.register(VartaCollector(varta_host, varta_port))
    while True:
        # period between collection
        time.sleep(frequency)
