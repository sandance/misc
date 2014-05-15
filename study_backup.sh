#!/bin/bash



studyname=$1
pdepath=$2
postpde=$3
od_account=$4
osticket=$5

cluster=$6
volume=$7

temp_dir=/mnt/$volume/atp/temp/$osticket



usage()
{
	echo "$0 <studyname> <pde_path> <postpde_path> <od_acount> <ticketnum> <san/bb> <glusterfs/ibmlun2,3> <volume>"
        echo "-----------------------------------------------"
}


group_files_for_san()
{
	mkdir -p $temp_dir
	echo "$temp_dir has been created"
	mkdir -p $temp_dir/{OD,user}
	cp -rf 	$postpde/output/{HomeWorkGroup,HomeWorkAll,Penetration,GenerateTripLegs,GenerateTripLegsSubDAG,GenerateHomeWorkMatrix,GenerateTripLegMatrix,CombineTripLegs,ClassifySubscribers,PackageODStudy,ClassifyPointsDayGroup,ClassifyPointsDay,PackageClassifiedPoints}  $temp_dir/OD/ 					#copy od study output, volume=static2/od or ibmlun2 
	sudo cp -rf  /opt/home/$od_account/atp  $temp_dir/user/    #copy user account config files  
	echo "grouping done "
}

send_to_san()
{

	cd  /mnt/$volume/atp/temp/
	tar -c $osticket/  -f - | ssh nazmul@10.255.210.253 " cat > /opt/odstudies/CURRENT/${osticket}.tar " 
#	rm -rf $study_path

#:%s/\/mnt\/$cluster\/$volume\/temp\/$osticket\//temp_dir/g
}

# Do the work

if [ $# -ne 8 ]
then
        usage
        exit 0
fi

case $cluster in
        san )
                group_files_for_san 
		send_to_san 	;;
        bb )
            #   send_to_bb ;;

esac
