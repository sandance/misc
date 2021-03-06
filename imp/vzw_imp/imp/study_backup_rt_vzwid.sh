#!/bin/bash



studyname=$1
postpde=$2
pde=$3
ticket=$4
account=$5
disk=$6
volume=$7


temp_dir=/mnt/glusterfs/$volume/atp/temp/$ticket

usage()
{
	echo "$0 <studyname> <postpde_path> <pde_path> <ticket> <account> <disk> <vol>"
        echo "-----------------------------------------------------------------------------"
}


#group_files_for_san()
#{
#	ssh nazmul@10.255.210.253 "mkdir -p /opt/odstudies/CURRENT/$ticket/{OD,config}"
#	rsync -avz  $postpde/output/{HomeWorkGroup,HomeWorkAll,Penetration,GenerateTripLegs,GenerateTripLegsSubDAG,GenerateHomeWorkMatrix,GenerateTripLegMatrix,CombineTripLegs,ClassifySubscribers,PackageODStudy,ClassifyPointsDayGroup,ClassifyPointsDay,PackageClassifiedPoints}  nazmul@10.255.210.253:/opt/odstudies/CURRENT/$ticket/OD/ 

#	rsync -avz /opt/home/$account/  nazmul@10.255.210.253:/opt/odstudies/CURRENT/$ticket/config/

#	ssh nazmul@10.255.210.253 "tar -cv --remove-files -f /opt/odstudies/CURRENT/${ticket}.tar /opt/odstudies/CURRENT/$ticket/ "

#}


group_files_for_san()
{
	mkdir -p $temp_dir
	echo "$temp_dir has been created"
	mkdir -p $temp_dir/OD
	cp -rf 	$postpde/output/{PackageODStudy,PackageClassifiedPoints}  $temp_dir/OD/ 					#copy od study output, volume=static2/od or ibmlun2 
#	sudo cp -rf  /opt/home/$account/atp  $temp_dir/user/    #copy user account config files  
	echo "grouping done "
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
send_to_san
