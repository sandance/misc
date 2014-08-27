#!/bin/bash

HOST_IP=$(ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}')
HOSTNAME=$(hostname) # not required actually

# get the gluster bricks

BRICKS=$(gluster volume status dell2 | grep $HOST_IP  | cut -d":" -f2 | cut -d"/" -f1-4`)

#Now for each gluster brick get the disk space
echo -e "Filesystem\tSize Used Avail\tDisk\t\tUse%"
for gsbrick in BRICKS
do
	percent=$(df -h $gsbrick/brick1/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5,$1 }' | cut -d'%' -f1)
	alex_info=$(df -h /gluster_bricks/dell2/brick1/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $2,$3,$4}')
	drive=$(df -h /gluster_bricks/dell2/brick1/ | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $1 }')
	echo -e "$HOST_IP\t$alex_info\t$drive\t$percent"
done
	



