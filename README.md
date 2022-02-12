<h1 align="center"> PyNetFuzz</h1>
<div align="center">
    <img alt="Version" title="Package Version" src="https://img.shields.io/badge/PyNetFuzz-v1.0.0-blue">
    <img alt="Version" title="Package Coverage" src="https://img.shields.io/badge/coverage-75%25-green">
    <img alt="Version" title="Package License" src="https://img.shields.io/badge/license-MIT-lightgrey">
</div>

## Summary

Package to create a Fuzz testing environment on a local network with randomised and configurable packet parameters.

---

## Contents

* [About](#about)
  * [Features](#features)
  * [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)
  * [CommandLine](#commandline)
  * [Arguments](#arguments)
  * [Install](#install)
* [Project](#project)
  * [Status](#status)
  * [Todo](#todo)
  * [Licence](#licence)

---

## About

### Features

Fully customisable packets and automated packet randomness:

* Customisable MAC addresses endpoints (`Layer 2`), Network layer endpoints and protocols (`Layer 3`), Transport layer endpoints and protocols (`Layer 4`), Network cast communication, packet length and more.
* Distinguishable `Source` and `Destination` addresses, ports and more.
* Fully randomisable Ethernet frame structure and features
* Random visible seed for repeatable packets and payloads

### Technologies

* Python: 3.8+
* scapy: 2.4.5
* psutils: 5.8.0

---

## Setup

Download and install package to Python environment

```CLI
python setup.py install
```

---

## Usage

### Commandline

```CLI
python pynetfuzz.py <Target IP> <Network interface> <N packets> [source_ip] [target_mac] [source_mac] [target_port] [source_port] [int_protocol] [trans_protocol] [cast] [headers] [vlan] [min_packet] [max_packet] [seed]
```

### Arguments

```CLI
Positional arguments
target_ip (str): IP address of target on network
network_interface (str): Name of the interface connected to the local network
n_packets (int): Number of packets to be sent

Optional arguments
source_ip [-sip]  IP address of source on network (default: Random)
target_mac [-tm]  MAC address of target on network [Self / valid MAC address] (default: Random)
source_mac [-sm]  MAC address of source on network [Self / valid MAC address] (default: Random)
target_port [-t_p]  Port of target on network (default: Random)
source_port [-s_p]  Port of source on network (default: Random)
int_protocol [-ip]  Specify the internet protocol [IPv4 / IPv6] (default: Random)
trans_protocol [-tp]  Specify the transport protocol [TCP / UDP] (default: Random)
cast [-c]  Specify cast types [unicast / multicast / broadcast] (default: Random)
headers [-hd]  Disable randomised headers (default: Random)
vlan [-vl]  Adds vlan tag
min_length [-min]  Specify minimum packet length (default: Ethertype minimum)
max_length [-max]  Specify maximum packet length (default: Ethertype maximum)
seed [-s]  Specify seed to generate packets (default: Random seed)
```

---

## Project

### Status

* In development

### Todo

* [ ] Add Jumbo frames
* [ ] Improve performance

### Licence

> License can be found [here](./LICENSE)
