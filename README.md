[![Join the chat at https://gitter.im/QualiSystems/cloudshell-recorder](https://badges.gitter.im/QualiSystems/cloudshell-recorder.svg)](https://gitter.im/QualiSystems/cloudshell-recorder?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/QualiSystems/cloudshell-recorder.svg?branch=develop)](https://travis-ci.org/QualiSystems/cloudshell-recorder) [![Coverage Status](https://coveralls.io/repos/github/QualiSystems/cloudshell-recorder/badge.svg?branch=dev)](https://coveralls.io/github/QualiSystems/scloudshell-recorder?branch=dev) 
[![PyPI](https://img.shields.io/pypi/pyversions/cloudshell-recorder.svg?maxAge=2592000)]() [![PyPI](https://img.shields.io/pypi/v/cloudshell-recorder.svg?maxAge=2592000)]()
[![Dependency Status](https://dependencyci.com/github/QualiSystems/cloudshell-recorder/badge)](https://dependencyci.com/github/QualiSystems/cloudshell-recorder)

---

![quali](quali.png)

# Cloudshell Recorder

Command line utility to create devices SNMP recordings.

## Installing
```
$ python -m pip install cloudshell-recorder
```
Or you are welcome to download compiled ```cloudshell_recorder.exe``` from one of our [Releases](https://github.com/QualiSystems/cloudshell-recorder/releases)
## Usage
```
$ cloudshell-recorder new 127.0.0.1
```
### SNMP Recordings
To create recording using SNMP v2 or v1 run the following command:
```
$ cloudshell-recorder new 127.0.0.1 --snmp-record-type=snmp --snmp-community=public
```
For SNMP v3:
```
$ cloudshell-recorder.exe new 192.168.42.235 --snmp-record-type=snmp --snmp-user=snmp_user_v3 --snmp-password=Password1 --snmp-private-key=Password2 --snmp-auth-protocol=SHA --snmp-priv-protocol=DES --destination-path=.\ --snmp-bulk
```
More information available in app help:
```
$ cloudshell-recorder new --help
```

## License
[Apache License 2.0](https://github.com/QualiSystems/cloudshell-recorder/blob/dev/LICENSE)