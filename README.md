# eso-tpsys-client

##

Run with ```./tpsys_client/launch.ssh``` from the tpsys home folder

## Install 

This is for Python 2.7

As root user:

```
$ su root
$ sudo apt-get install git curl screen vim -y
$ touch /var/log/tpsys_bridge_client.log
$ chmod -R a+rw /var/log/tpsys_bridge_client.log
$ curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py
$ python get-pip.py
$ rm get-pip.py
$ pip install --upgrade pip
```

As tpsys user:

```
$ su tpsys
$ git clone https://github.com/elexess/eso-tpsys-bridge-client.git tpsys_bridge
$ cd tpsys_bridge
$ pip install -r requirements.txt
```

## Set the Environment Variables

```
$ cp .env.sample .env
$ vim .env
```

This is an example for MDE01:

```
export ESO_WATCHDOGPATH=/home/tpsys/tpsys_bridge/watchdog.py
export ESO_ERP_HOST=erp.eso-electronic.com
export ESO_BRIDGE_LOCAL_IP=10.1.0.5
export ESO_BRIDGE_HOST=10.1.0.5
export ESO_BRIDGE_HOST_PORT=10.1.0.5:8080
export ESO_MACHINE_NAME=MDE01
export ESO_MACHINE_SERIAL_NUMBER=130276
export ESO_MACHINE_IP=10.1.0.35
export ESO_BRIDGE_NAME=B-TP-01
```
