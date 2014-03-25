#!/bin/bash

StudyName=$1 # Give study name 
OD_VOLUME=$2 # Give study volume /od/old or hp
your_need=$3 # first or second 
study_starts=$4
study_ends=$5
executiondir=exec_${study_starts}-${study_ends}


usage() {
	echo "Usage: $0 <StudyName> <OD Volume> <first/second> <start_date> <end_date>"
	echo "------------------------------------------------------------------------"
}

if [ $# -ne 5 ]
then
	usage
	exit 1
fi
	


create_dir() {
	sudo mkdir -m a=rwx -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/$executiondir/input
	sudo mkdir -m a=rwx -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/$executiondir/output
	sudo mkdir -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/$executiondir/sla
	sudo chown nobody.nobody /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/$executiondir/sla	
        sudo chmod go+rwx /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/$executiondir/input/
        sudo chmod go+rwx /mnt/glusterfs/$OD_VOLUME/atp/$StudyName	
}

install_packages()
{

cat << 'EOF' >> ~/.bashrc
export PYTHONPATH=/opt/python2.7.3/lib/python2.7/site-packages/
export LD_LIBRARY_PATH=/opt/python2.7.3/lib
export PATH=/opt/python2.7.3/bin:$PATH
export LD_LIBRARY_PATH=/opt/gdal-1.9.1/lib/:/opt/boost-1.50.0/lib:/opt/gcc/lib64/:/opt/gcc/lib:$LD_LIBRARY_PATH
EOF

sleep 1 

source ~/.bashrc

sleep 1

pip install --user --no-index -f http://mega/pip/ genshi
sleep 2
pip install --user --no-index -f http://mega/pip/ six
sleep 2
pip install --user --no-index -f http://mega/pip/ pyDatalog
sleep 2


}


create_dir_inside ()
{

mkdir -p ~/atp/$StudyName/$executiondir/input
cd ~/atp/$StudyName/$executiondir/input
# create the dagjobs.cfg file
touch dagjobs.cfg
mkdir -p work

sleep 1

cat  >> ~/atp/$StudyName/$executiondir/input/dagjobs.cfg << EOL
--pkg_bc_od
bc-11.0.0-0-g895fd6f.sxb
--pkg_metrics
metrics-11.0.0-0-g895fd6f.tar.gz
--pkg_parser
cdma-11.0.0-0-g895fd6f.tar.gz
--pkg_pde
pdeloc-11.0.0-0-g895fd6f.sxb
--pkg_odd
clustering-11.0.0-0-g895fd6f.tar.gz
--pkg_od
od-11.0.0-0-g895fd6f.sxb
EOL
}


post_dagjobs ()
{
	wget http://10.255.3.20/pkg/dld_bootstrap
	chmod u+x dld_bootstrap
	sleep 1
	./dld_bootstrap dagjobs.cfg
}





echo "./study_setup.sh <StudyName> <volumeName>"

case $your_need in 
	first  )
		create_dir ;;
	second )
		install_packages 
		create_dir_inside 
		post_dagjobs ;;

esac 
	

echo "\neverything done\n "
