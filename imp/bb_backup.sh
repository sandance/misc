#!/bin/bash



studyname=$1
pdepath=$2
postpde=$3
od_account=$4
osticket=$5
#cluster=$6
#volume=$7
disk=$6 #disk31 or disk32 like that
#temp_dir=/mnt/glusterfs/$volume/atp/temp_bb/$osticket

bb_disk=/study/$disk/

usage()
{
	echo "$0 <studyname> <pde_path> <postpde_path> <od_acount> <ticketnum> <disk>"
        echo "-----------------------------------------------"
}


send_files_for_bb()
{
        ssh nazmul@10.255.211.26  "mkdir -p $bb_disk/$osticket/$studyname/{OD,user,pde}"      # create the dirs in remote folder
	
        rsync -avz  $postpde/output/{HomeWorkGroup,HomeWorkAll,Penetration,GenerateTripLegs,GenerateTripLegsSubDAG,GenerateHomeWorkMatrix,GenerateTripLegMatrix,CombineTripLegs,ClassifySubscribers,PackageODStudy,ClassifyPointsDayGroup,ClassifyPointsDay,PackageClassifiedPoints}  nazmul@10.255.211.26:$bb_disk/$osticket/$studyname/OD/                                         #copy od study output, volume=static2/od or ibmlun2 
        rsync -avz  /opt/home/$od_account/atp  nazmul@10.255.211.26:$bb_disk/$osticket/$studyname/user/    #copy user account config files 
	rsync -avz  $pdepath/*  nazmul@10.255.211.26:$bb_disk/$osticket/$studyname/pde/                    # send pde files in BB

	#tar the file in remote dir
#	ssh nazmul@10.255.211.26 "tar -zcvf $bb_disk/${studyname}.tar   $bb_disk/$studyname" && ssh nazmul@10.255.211.26 "rm -rf $bb_disk/$studyname " 
	echo "$studyname has copied to BB"
}

#send_to_bb()
#{
#	cd  /mnt/glusterfs/$volume/atp/temp_bb/
#	tar -zc $osticket/  -f - | ssh nazmul@10.255.211.26 " cat > /study/$disk/study_backup/${osticket}.tgz " 
#	rm -rf $osticket/
#}
# Do the work

if [ $# -ne 6 ]
then
        usage
        exit 0
fi

send_files_for_bb
