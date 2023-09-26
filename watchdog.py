import time
import os
import httplib
from string import find
import re
import logging
from machine_config import *

# Setting log verbosity
logging.basicConfig(level=logging.INFO,
    filename='/var/log/tpsys_bridge_client.log',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info("Start watchdog")

# Settings
logging.info("Load environment variables from machine_config.py file")
MACHINE_LOGFILE = r"/home/tpsys/log/mhproc/log"

# Print Launch config
print("Starting TPSys Bridge Client Watchdog")
print("Observe the log file live with '$ less +F /var/log/tpsys_bridge_client.log'")
print("\n")
print("Launch Configuration:")
print(" - Machine Name: " + MACHINE_NAME)
print(" - Machine Serial Number: " + MACHINE_SERIAL_NUMBER)
print(" - Machine IP: " + MACHINE_IP)
print(" - ERPNext Host: " + ERP_HOST)
print(" - Bridge IP: "+ BRIDGE_LOCAL_IP)
print("\n")

# Init Start Values
CAN_PROCESS = 0
f = open(MACHINE_LOGFILE, 'r')

def add2str(pr, ne):
    """Helper to concat"""
    return pr + ne

def broadcast_action(action, slot, type, serial, feeder, x, y , yvalid, angle):
    """Make post request to local brigde"""
    conn = httplib.HTTPConnection(BRIDGE_LOCAL_IP)
    params = ''
    params = add2str(params, '?mc_ip='+ MACHINE_IP)
    params = add2str(params, '&mc_name='+ MACHINE_NAME)
    params = add2str(params, '&mc_serial='+ MACHINE_SERIAL_NUMBER)
    params = add2str(params, '&action='+ action)
    params = add2str(params, '&mg_serial='+serial)
    params = add2str(params, '&slot='+ slot)
    params = add2str(params, '&type='+ type)
    params = add2str(params, '&feeder='+ feeder)
    params = add2str(params, '&cl_x='+ x)
    params = add2str(params, '&cl_y='+ y)
    params = add2str(params, '&cl_angle='+ angle)
    logging.info("Making post to bridge" + BRIDGE_LOCAL_IP + "/machine/action" + str(params))
    conn.request("POST", "/machine/action" + params)


def process_action(line):
    """Process new line (new action)"""
    logging.info("New line in log file recognized")
    sline = line.split()
    action = None
    slot = 'NA'
    type = 'NA'
    serial = 'NA'
    feeder = 'NA'
    x = 'NA'
    y = 'NA'
    yvalid = 'NA'
    angle = 'NA'
    if not line:
         return
    if 'TEX' in sline:
         logging.info("tex")
         return
    if find(sline[1], 'MIMHButtonPressed') >= 0:
        action = 'BTN' # Button Pressed
        slot = re.findall(r'\d+', sline[2])[0]
        logging.info("Button pressed recognized")
    if find(sline[1], 'MIMHMagRemoved') >= 0:
        action = 'MR' # Magazine Removed
        slot = re.findall(r'\d+', sline[2])[0]
        logging.info("Magazine removed recognized")
    if find(sline[1], 'insertMag') >=0 :
        action = 'MI' # Magazine Inserted
        info = re.findall(r'\d+', sline[1])
        slot = info[4]
        type = info[3]
        serial = info[2]
        logging.info("Magazine insert recognized")
    if action:
        broadcast_action(action, slot, type, serial, feeder, x, y , yvalid, angle)


CAN_PROCESS = 0
while 1:
    line = f.readline()
    if not line:
        # Reread all old lines, set flag CAN_PROCESS
        # sleep 1 sec
        CAN_PROCESS = 1
        time.sleep(1)
    else:
        if CAN_PROCESS:
           logging.info("Debug" + str(line.split()))
           process_action(line)
