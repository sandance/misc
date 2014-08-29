#!/bin/bash

BRICKS=$@

HOST_IP=$(/sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}')
HOSTNAME=$(hostname) # not required actually


#Now for each gluster brick get the disk space
echo -e "Filesystem\tSize Used Avail\tDisk\t\tUse%"

for gsbrick in $BRICKS
do
	percent=$(df -h $gsbrick/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5,$1 }' | cut -d'%' -f1)
	alex_info=$(df -h /gluster_bricks/dell2/brick1/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $2,$3,$4}')
	drive=$(df -h /gluster_bricks/dell2/brick1/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $1 }')
	echo -e "$HOST_IP\t$alex_info\t$drive\t$percent"
done
