#!/bin/bash

StudyName=$1 # Give study name 
OD_VOLUME=$2 # Give study volume /od/old or hp
your_need=$3

create_dir() {
	sudo mkdir -m a=rwx -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/input/work
	sudo mkdir -m a=rwx -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/output
	sudo mkdir -p /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/sla
	sudo chown nobody.nobody /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/sla	
        sudo chmod go+rwx /mnt/glusterfs/$OD_VOLUME/atp/$StudyName/input/
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
bc-production_hotfixes-8-g5dfac3f.sxb
--pkg_metrics
metrics-hotfix-0-g54a0af6.tar.gz
--pkg_parser
cdma-parser-0.3.4-0-g956abbb.tar.gz
--pkg_pde
pdeloc-9.2.0-31-g6c27c7f.sxb
--pkg_odd
odd-0.9.2-beta-14-gbcfea2b.tar.gz
--pkg_od
od_0.9.2-beta-14-gbcfea2b.sxb
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
