<h1 align="center"> PyNetFuzz </h1> <br>
<p align="center">
  <a href="https://gitpoint.co/">
    <img alt="GitPoint" title="GitPoint" src="http://i.imgur.com/VShxJHs.png" width="450">
  </a>
</p>

<p align="center">
  GitHub in your pocket. Built with React Native.
</p>

<p align="center">
  <a href="https://itunes.apple.com/us/app/gitpoint/id1251245162?mt=8">
    <img alt="Download on the App Store" title="App Store" src="http://i.imgur.com/0n2zqHD.png" width="140">
  </a>

  <a href="https://play.google.com/store/apps/details?id=com.gitpoint">
    <img alt="Get it on Google Play" title="Google Play" src="http://i.imgur.com/mtGRPuM.png" width="140">
  </a>
</p>
<p align="center">
    <a>
    <img alt="Version" title="Package Version" src="https://img.shields.io/badge/PyNetFuzz-v1.0.0-blue" width="120">
    </a>
    <a>
    <img alt="Version" title="Package Coverage" src="https://img.shields.io/badge/coverage-75%25-green" width="120">
    </a>
    <a>
    <img alt="Version" title="Package License" src="https://img.shields.io/badge/license-MIT-lightgrey" width="120">
    </a>
</p>

![Version](https://img.shields.io/badge/PyNetFuzz-v1.0.0-blue)
![Coverage](https://img.shields.io/badge/coverage-75%25-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

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
```
python -m setup

---
## Usage
### Commandline
* To be done
### Arguments
* To be done
### Install
* To be done
---
## Project
### Status
* In development
### Todo
- [ ] Add Jumbo frames
- [ ] Improve performance
### Licence
> License can be found [here](./LICENSE)
