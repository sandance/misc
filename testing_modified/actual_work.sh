#!/bin/bash

create_condor_job()
{

IP=$1
machine=$2

shift 2
BRIK=$@


DIR=/home/airsageops/testing/work/$IP/
mkdir -p $DIR

cat <<EOF > $DIR/job_${IP}.condor
notification = Error
notify_user =  nislam@airsage.com
Executable  =  /home/airsageops/testing/script/disk_check.sh
Arguments       = $BRIK
Universe        = vanilla
Error           = $DIR/job-${IP}.err
Output          = $DIR/job_${IP}.out
Log             = $DIR/job_${IP}.log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = /home/airsageops/testing/script/disk_check.sh

Requirements = (( Machine=="$machine" ))
Queue
EOF
}



LOGFILE=/home/airsageops/testing/gluster.log
HOSTS=/home/airsageops/testing/hosts.txt

>$LOGFILE

ssh -t  airsageops@10.255.210.101 "sudo  /usr/sbin/gluster volume info all  | grep brick "  | tee -a $LOGFILE

cnt=0
while read ip host etc
do
	VOLUMES=$(cat $LOGFILE | grep brick | cut -d":" -f3 | awk -F"/" '{ print $3 }'| uniq)
        BRICKS=$(cat $LOGFILE | grep $ip  |  cut -d":" -f1,3 | cut -d"/" -f1-4 )
	#unset BRICKS
	#BRICKS=""
	create_condor_job $ip $host "$BRICKS"
	unset BRICKS
done < $HOSTS


## dag


find work/ -type f -name "*.condor" | awk '{print "JOB number-"NR" "$0}' > disk_check.dag
cat <<EOF >> disk_check.dag
DAGMAN_MAX_JOBS_IDLE=100
DAGMAN_MAX_JOBS_SUBMITTED=400
EOF





#create_condor_job()
#{
#
#IP=$1
#machine=$2
#BRICKS=$3
#
#DIR=/home/airsageops/testing/work/$IP/
#mkdir -p $DIR
#
#cat <<EOF > $DIR/job_${IP}.condor
#notification = Error
#notify_user =  nislam@airsage.com
#Executable  =  /home/airsageops/testing/script/disk_check.sh
#Arguments       = $BRICKS
#Universe        = vanilla
#Error           = $DIR/job-${IP}.err
#Output          = $DIR/job_${IP}.out
#Log             = $DIR/job_${IP}.log
#
#should_transfer_files = YES
#when_to_transfer_output = ON_EXIT
#transfer_input_files = /home/airsageops/testing/script/disk_check.sh
#
#Requirements = (( Machine=="$machine" ))
#Queue
#EOF
#}	
	
