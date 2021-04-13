#!/bin/bash

# General Settings
WATCHDOGPATH='/home/tpsys/watchdog.py'
ERP_HOST='erp.eso-electronic.com'
BRIGDE_HOST='192.168.100.5'

# Make sure that not screen session are forgotten
killall screen

echo "[OK] TPSys Bridge started, Press [CTRL+C] to stop ..."

# Traping Ctrl + C
trap ctrl_c INT
function ctrl_c() {
        killall screen
        echo "Killing all 'screen' sessions"
        exit 0
}
COUNT=4
DEF=0 # If no ping set as default value zero
while :
do
    echo -ne "\r\r\r\r\r"
    echo -ne "$(date): "
    # Make sure python watchdog is running on the background
    if ! screen -list | grep -q "watchdog"; then
     screen -dm -S watchdog bash -c "python $WATCHDOGPATH"
    fi
    # Is ERP alive?
    countERP=$(ping -c $COUNT $ERP_HOST | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
    if [ ${countERP:-$DEF} -eq 0 ]; then
        # 100% failed
        echo -ne "[DOWN] $ERP_HOST, "
    else
        echo -ne "[UP] $ERP_HOST, "
    fi
    # Is bridge alive?
    countBridge=$(ping -c $COUNT $BRIGDE_HOST | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
    if [ ${countBridge:-$DEF} -eq 0 ]; then
        # 100% failed
        echo -ne "[DOWN] $BRIGDE_HOST"
    else
        echo -ne "[UP] $BRIGDE_HOST"
    fi
    sleep 1
done
