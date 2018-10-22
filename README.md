[![Build Status](https://travis-ci.org/QualiSystems/cloudshell-recorder.svg?branch=dev)](https://travis-ci.org/QualiSystems/cloudshell-recorder) [![Coverage Status](https://coveralls.io/repos/github/QualiSystems/cloudshell-recorder/badge.svg?branch=dev)](https://coveralls.io/github/QualiSystems/cloudshell-recorder?branch=dev) 
[![PyPI](https://img.shields.io/pypi/pyversions/cloudshell-recorder.svg?maxAge=2592000)]() [![PyPI](https://img.shields.io/pypi/v/cloudshell-recorder.svg?maxAge=2592000)]()
[![Dependency Status](https://dependencyci.com/github/QualiSystems/cloudshell-recorder/badge)](https://dependencyci.com/github/QualiSystems/cloudshell-recorder)

---

![quali](https://github.com/QualiSystems/shellfoundry/blob/master/quali.png)

# Cloudshell Recorder

The CloudShell Recorder is a command line utility tool used to record customer device responses to certain SNMP commands, for troubleshooting purposes. 

## Installing the CloudShell Recorder
- Using pip: ```$ python -m pip install cloudshell-recorder```,
- Download the compiled ```cloudshell_recorder.exe``` file from one of our [Releases](https://github.com/QualiSystems/cloudshell-recorder/releases)

### Producing an SNMP Recordings
To generate a recording, run one of the following commands depending on your SNMP version: 
```
$ cloudshell-recorder new 127.0.0.1 --record-type=snmp --snmp-community=public
```
For SNMP v3:
```
$ cloudshell-recorder.exe new 192.168.42.235 --record-type=snmp --snmp-user=snmp_user_v3 --snmp-password=Password1 --snmp-private-key=Password2 --snmp-auth-protocol=SHA --snmp-priv-protocol=DES --destination-path=.\ --snmp-bulk
```
## CloudShell Recorder Help 

For additional information, run the following command to view the CloudShell Recorder help file: 
```
$ cloudshell-recorder new --help
```

## License
The CloudShell Recorder is licensed under the [Apache License 2.0](https://github.com/QualiSystems/cloudshell-recorder/blob/dev/LICENSE).
