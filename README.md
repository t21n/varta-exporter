# varta-exporter

[![Docker Pulls](https://img.shields.io/docker/pulls/tools4homeautomation/varta-exporter)](https://hub.docker.com/r/tools4homeautomation/varta-exporter/)
[![Docker Stars](https://img.shields.io/docker/stars/tools4homeautomation/varta-exporter.svg)](https://hub.docker.com/r/tools4homeautomation/varta-exporter/)

Read values from various VARTA batteries and provide es prometheus exporter metrics

Add a file `/etc/varta/config.yml` e.g.:
```
port: 3000
scrape_frequency: 1
varta_host: 192.168.0.23
varta_port: 502
```

Then you get something like this:
```
...
# HELP varta_installed_capacity installed capacity in Wh
# TYPE varta_installed_capacity gauge
varta_installed_capacity 586.0
# HELP varta_state_of_charge total state of charge in %
# TYPE varta_state_of_charge gauge
varta_state_of_charge 98.0
# HELP varta_total_charged_energy total charged energy in kWh
# TYPE varta_total_charged_energy gauge
varta_total_charged_energy 98.0
# HELP varta_from_grid_power energy from grid to home in W
# TYPE varta_from_grid_power gauge
varta_from_grid_power 0.0
# HELP varta_to_grid_power energy from home to grid in W
# TYPE varta_to_grid_power gauge
varta_to_grid_power 351.0
# HELP varta_charge_cycle_counter_total charge load cycles from
# TYPE varta_charge_cycle_counter_total counter
varta_charge_cycle_counter_total 0.0
# HELP varta_bat_state state of system: BUSY, RUN, CHARGE, DISCHARGE, STANDBY, ERROR, PASSIVE, ISLANDING
# TYPE varta_bat_state gauge
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 1.0
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 0.0
varta_bat_state{varta_bat_state="state"} 0.0

```