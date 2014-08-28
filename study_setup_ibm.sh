#!/bin/bash


usage () {
	echo "$0 <studyname> <OD_volume> <need,first/second>"
	echo "-----------------------------------------------"
}

if [ $# -ne 3 ]
then
	usage
	exit 1
fi






StudyName=$1 # Give study name 
OD_VOLUME=$2 # Give study volume /ibmlun1 ibmlun2 etc
your_need=$3 # first or second 

create_dir() {
	sudo mkdir -m a=rwx -p /mnt/$OD_VOLUME/atp/$StudyName/input/work
	sudo mkdir -m a=rwx -p /mnt/$OD_VOLUME/atp/$StudyName/output
	sudo mkdir -p /mnt/$OD_VOLUME/atp/$StudyName/sla
	sudo chown nobody.nobody /mnt/$OD_VOLUME/atp/$StudyName/sla	
        sudo chmod go+rwx /mnt/$OD_VOLUME/atp/$StudyName/input/
        sudo chmod go+rwx /mnt/$OD_VOLUME/atp/$StudyName	
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

mkdir -p ~/atp/$StudyName/input
cd ~/atp/$StudyName/input
# create the dagjobs.cfg file
touch dagjobs.cfg
mkdir -p work

sleep 1

cat  >> ~/atp/$StudyName/input/dagjobs.cfg << EOL
--pkg_bc_od
atp_batch-11.3.0-0-gbee6fe9.sxb
--pkg_metrics
metrics-11.3.0-0-gbee6fe9.tar.gz
--pkg_odd
clustering-11.3.0-0-gbee6fe9.tar.gz
--pkg_pde
pdeloc-11.3.0-0-gbee6fe9.sxb
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
