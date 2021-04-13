#!/bin/bash

# Colors

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

# Make sure that not screen session are forgotten, this is safe because tpsys doesn't utilize screen
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
     screen -dm -S watchdog bash -c "python $ESO_WATCHDOGPATH"
    fi
    # Is ERP alive?
    countERP=$(ping -c $COUNT $ESO_ERP_HOST | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
    if [ ${countERP:-$DEF} -eq 0 ]; then
        # 100% failed
        echo -ne "${RED}[ERP DOWN] $ESO_ERP_HOST ${ENDCOLOR}"
    else
        echo -ne "${GREEN}[ERP UP] $ESO_ERP_HOST ${ENDCOLOR}"
    fi
    # Is bridge alive?
    countBridge=$(ping -c $COUNT $ESO_BRIDGE_HOST | grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
    if [ ${countBridge:-$DEF} -eq 0 ]; then
        # 100% failed
        echo -ne "${RED}[BRIDGE DOWN] $ESO_BRIDGE_HOST ${ENDCOLOR}"
    else
        echo -ne "${GREEN}[BRIDGE UP] $ESO_BRIDGE_HOST ${ENDCOLOR}"
    fi
    sleep 1
done
