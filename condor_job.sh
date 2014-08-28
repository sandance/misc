#!/bin/bash

IP=$1
machine=$2


DIR=/home/airsageops/testing/work/$IP/
mkdir -p $DIR

cat <<EOF > $DIR/job_${IP}.condor
notification = Error
notify_user =  nislam@airsage.com
Executable  =  /opt/home/airsageops/testing/script/disk_check.sh
Universe        = vanilla
Error           = $DIR/job-${IP}.err
Output          = $DIR/job_${IP}.out
Log             = $DIR/job_${IP}.log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = /opt/home/airsageops/testing/script/disk_check.sh

Requirements = (((asg_blacklist != true) && Machine=="$machine"))
Queue
EOF
