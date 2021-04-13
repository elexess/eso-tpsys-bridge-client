import time
import httplib

# Settings
MACHINE_SERIAL = os.environ['ESO_MACHINE_SERIAL']
BRIDGE_NAME = "B-TP-01"
BRIDGE_LOCAL_IP = os.environ['ESO_BRIDGE_HOST_PORT']

while 1:
    conn = httplib.HTTP(BRIDGE_LOCAL_IP)
    conn.request("POST", "/machine/connection/ping" + '?bridge_name='+ BRIDGE_NAME +'&mc_serial=' + MACHINE_SERIAL)
    time.sleep(30)
