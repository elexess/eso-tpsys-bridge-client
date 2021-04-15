# eso-tpsys-client

## Install 

This is for Python 2.7

```
$ su root
$ sudo apt-get install git curl screen -y
$ touch /var/log/tpsys_bridge_client.log
$ chmod -R a+rw /var/log/tpsys_bridge_client.log
$ python get-pip.py
$ pip install --upgrade pip
$ su tpsys
$ git clone https://github.com/elexess/eso-tpsys-bridge-client.git $ $ cd tpsys_bridge
$ pip install -r requirements.txt
```

## Set the Environment Variables

This is an example for MDE01:

```
export ESO_WATCHDOGPATH=/home/tpsys_bridge/watchdog.py
export ESO_ERP_HOST=erp.eso-electronic.com
export ESO_BRIDGE_HOST=192.168.100.5
export ESO_BRIDGE_HOST_PORT=192.168.100.5:8080
export ESO_MACHINE_NAME=MDE01
export ESO_MACHINE_SERIAL=130276
export ESO_MACHINE_IP=192.168.100.210
```