#!/bin/bash

# This file create condor file for Preparelegacy opt out counts

msc=$1 # switch name
day=$2 
path_to_study=$3

DIR=work/$msc/$day
mkdir -p $DIR
# inside each $msc/$day/msc-day.condor file 

cat <<EOF > $DIR/$msc-${day}_pde.condor
notification = Error  
notify_user =  nislam@airsgae.com  
Executable      = /opt/home/pde9_condor/test/count_pde_subs.py 
Arguments       = ${msc}_${day}.csv.gz 
Universe        = vanilla  
Error           = $DIR/$msc-${day}_pde.err 
Output          = $DIR/$msc-${day}_pde.out  
Log             = $DIR/$msc-${day}_pde.log 
 
should_transfer_files = YES  
when_to_transfer_output = ON_EXIT  
transfer_input_files = /opt/home/pde9_condor/test/count_pde_subs.py,$path_to_study/$msc/$day/${msc}_${day}.csv.gz 
 
  
request_cpus = 10  
request_disk = 10240 
Requirements = (asg_owner == "pde9_condor" || asg_owner == "free")  
  
Queue
EOF

#sleep 1
# Submitting dag man 

#find work/$msc/  "*.condor" |sort |xargs -n 1 condor_submit 

