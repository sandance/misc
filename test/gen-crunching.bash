#!/bin/bash
# Condor submit description file for pde

msc=$1
d=$2

DIR=work/$msc/$d
mkdir -p $DIR
cat <<EOF > $DIR/$msc-$d.condor
notification = Error
notify_user = dbello@airsage.com
Executable      = /home/od_cruncher/run_od_crunch.bash
Arguments       = -s $msc -d $d -c mobile_study_may.txt -i pdeloc-id_rsa -u analysis -m 10.255.2.107 -b /bfp/analysis/AtlCharStudy/June/$msc/ -p pdeloc_7.5.1.0-288-g2b74.sxb 
Universe        = vanilla
Error           = $DIR/$msc-$d.err
Output          = $DIR/$msc-$d.out
Log             = $DIR/$msc-$d.log

should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = /home/od_cruncher/catalogs/atlchar_study.txt,/home/od_cruncher/get_raw_data.bash,/home/od_cruncher/pde_install_and_run.bash,/home/od_cruncher/,/home/od_cruncher/run_od_crunch.bash,/home/od_cruncher/pdeloc_7.5.1.0-288-g2b74.sxb,/home/od_cruncher/backup_and_stats.bash,/home/od_cruncher/pdeloc-id_rsa,/home/od_cruncher/catalogs/mobile_study_may.txt

transfer_output_remaps = "${msc}_$d.stats = $DIR/${msc}_$d.stats"

+RequiresWholeMachine = True
Requirements = CAN_RUN_WHOLE_MACHINE
Queue
EOF
