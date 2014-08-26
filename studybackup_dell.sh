#!/bin/bash



studyname=$1
postpde=$2
pde=$3
ticket=$4
account=$5
disk=$7
volume=$6


temp_dir=/mnt/glusterfs/$volume/atp/temp/$ticket

usage()
{
	echo "$0 <studyname> <postpde_path> <pde_path> <ticket> <account> <disk> <vol>"
        echo "-----------------------------------------------------------------------------"
}




group_files_for_san()
{
	mkdir -p $temp_dir
	echo "$temp_dir has been created"
	mkdir -p $temp_dir/{OD,user,input}

	cp $postpde/input/* $temp_dir/input/

	cp -rf 	$postpde/output/{HomeWorkGroup,HomeWorkAll,Penetration,GenerateTripLegs,GenerateTripLegsSubDAG,GenerateHomeWorkMatrix,GenerateTripLegMatrix,CombineTripLegs,ClassifySubscribers,PackageODStudy,ClassifyPointsDayGroup,ClassifyPointsDay,PackageClassifiedPoints,VisibilityDayGrou}  $temp_dir/OD/ 					#copy od study output, volume=static2/od or ibmlun2 
	sudo cp -rf  /opt/home/$account/atp  $temp_dir/user/    #copy user account config files  
	echo "grouping done "
}


send_to_SL_and_BB()
{
	#cd /mnt/$volume/atp/temp/
	rsync -r  --no-p --no-o --no-g --progress /mnt/glusterfs/$volume/atp/temp/${ticket}  rsync://10.255.211.26:/study/$disk/
	cd /mnt/glusterfs/$volume/atp/temp/
	#tar --remove-files -cvf ${ticket}.tar  $ticket/
	#rsync -a  --no-p --no-o --no-g --progress  /mnt/glusterfs/$volume/atp/temp/${ticket}.tar rsync://10.255.211.46/ODSTUDIES/

	echo "study ${ticket} has been sent to 211.41"
	rm -rf /mnt/glusterfs/$volume/atp/temp/${ticket}*
	
	echo "study deleted"

	
}


send_to_san()
{

	cd  /mnt/glusterfs/$volume/atp/temp/
	tar -c $ticket/  -f - | ssh nazmul@10.255.210.253 " cat > /opt/odstudies/CURRENT/${ticket}.tar " 
	rm -rf $ticket/

#:%s/\/mnt\/$cluster\/$volume\/temp\/$ticket\//temp_dir/g
}



if [ $# -ne 7 ]
then
        usage
        exit 0
fi

group_files_for_san 
send_to_SL_and_BB
