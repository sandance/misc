#!/usr/bin/python


import sys
import os
import subprocess 
from subprocess import PIPE
from subprocess import check_output as qx
import calendar,datetime
import datetime
from datetime import datetime,timedelta,date



import month
from month import add_month


def date_converter(dates,flag):
        start_year=str(dates)[0:4]
        start_month=str(dates)[4:6]
        start_day=str(dates)[6:]
        return month.add_month(date(int(start_year),int(start_month),int(start_day)),flag)


def header(version):
	legacy_header={ 
'verizon' : '"line,sub1,dialeddigits,longitude,latitude,d2t,uncert,method,event,epoch,type_code,pr_mid,pr_cid,pr_sid,pr_donor,route_id,sub2,dummy1,dummy2,dummy3,dummy4,dummy5,dummy6,dummy7,dummy8,dummy9,dummy10"' ,
'sprint'  : '"line,sub1,dialeddigits,longitude,latitude,d2t,uncert,method,event,epoch,type_code,pr_mid,pr_cid,pr_sid,pr_donor,route_id,sub2"',
'ibm' : '"line,sub1,dialeddigits,longitude,latitude,d2t,uncert,method,event,epoch,type_code,pr_mid,pr_cid,pr_sid,pr_donor,route_id,sub2"' }
	return legacy_header[version.lower()]


def airsage_default(start_date,end_date,t_zone,fp):
		days=list()
		fp.write('[hwmrun]\n')
		fp.write('\tcounty=-f %d  %d -m county\n' % (int(start_date),int(end_date)))
		fp.write('\tzone=-f %d  %d -m zone\n'  % (int(start_date),int(end_date)))
		fp.write('[tlmrun]\n\n\n')

		days_matrix=['airsageWDDP','airsageWEDP','airsageDP9class','airsageWDH','airsageWEH']
		for index,each_matrix in enumerate(days_matrix):
			#airsageWEDP=subprocess.Popen(["python","testing_date_modified.py",start_date,end_date,'airsageWE'], stdout=PIPE)
			#days_list=subprocess.Popen(["python","testing_date_modified.py",start_date,end_date,each_matrix], stdout=PIPE)
			if index == 3:
				fp.write('[admrun]\n\n')
		
			days_list=""
			days_list=qx(["python","testing_date_modified.py",start_date,end_date,each_matrix])
			#for line in iter(days_list.stdout.readline,''):
			#	a=line # putting into a string format 
			a=days_list
			str_len=len(a)
			r=a[2:str_len-2] # trivial process, dont know how to make it nice
			for i in r.split(','):
				val=i.replace("'",'')
				days.append(val)
			#fp.write('--tlmrun\n')
			if each_matrix in ('airsageWDH','airsageWEH'):
                                fp.write('\t%s=' % each_matrix +'America/%s' % t_zone)
                        else:
				fp.write('\t%s=' % each_matrix +'America/%s' % t_zone)
			if each_matrix  in ('airsageWDDP', 'airsageWDH','airsageDP9class'):
				fp.write(' -g Tue Wed Thu -f ')
			else:
				fp.write(' -g Sat Sun -f ')
			fp.write(' '.join(str(v) for v in days))
			del days[:] # delete the list 
			if 'DP' in each_matrix: # that is dap part exist 
				fp.write(' -t 0000-0600-H00:H06 0600-1000-H06:H10  1000-1500-H10:H15 1500-1900-H15:H19 1900-2400-H19:H24')
			else:
				fp.write(' -t H')
			if each_matrix  in ('airsageDP9class'):
				fp.write(' -p 9-class --subscriber2class\n')
			else:
				fp.write(' --subscriber2class -p 3-class\n')

def get_switches(n):
	sw=set()
	for i in range(n):
		sw.add(raw_input());
	return sw



def display(fp):
	for i in fp:
		print i

def ask(str_input):
	print 'Enter %s' % str_input
	path=raw_input()
	return path


def time_utc(area):
	dict = { 'Chicago' : 'CST-06' , 'Los_Angeles' : 'PST-08' , 'Denver' : 'MST-07' , 'New_York' : 'EST-05','Anchorage': 'AKST-09' }
	return dict[area]


def switch_list(fp):
	num_sw=int(raw_input('number of switches?\n'))
	switches=set()
        switches=get_switches(num_sw)
	sw_list=",".join(str(i) for i in switches)
	fp.write('switch = %s' % sw_list) 
	fp.write('\n')

def penetration(start_date,end_date,carrier,fp):
	fp.write('[anlzsubrun]\n')
	if carrier.lower() == 'sprint' or 'ibm':
		fp.write('\tZ_adjusted_penetration = --min 4 --max 22 --min_avg_sight 180\n')
		fp.write('\tA_initial_all_subscribers = --min_avg_sight 180\n')
	elif carrier.lower() == 'verizon':
		fp.write('\tZ_adjusted_penetration = --min 3 --max auto  --filter %d  %d --min_avg_sight 180\n' % (int(start_date),int(end_date)))
		fp.write('\tA_initial_all_subscribers = --min_avg_sight 180\n')
		fp.write('\tM_date_range = --filter %d %d --min_avg_sight 180\n' % (int(start_date),int(end_date)))

def dagjobs(fp):
	fp.write('[packages]\n')
	fp.write('\tpkg_metrics = metrics-11.1.0-beta-49-g1c623cb.tar.gz\n')
	fp.write('\tpkg_odd = clustering-11.1.0-beta-49-g1c623cb.tar.gz\n')
	fp.write('\tpkg_od = od-11.1.0-beta-49-g1c623cb.sxb\n')
	fp.write('\tpkg_bc_od = bc-11.1.0-beta-49-g1c623cb.sxb\n')
	fp.write('\tpkg_pde = pdeloc-11.1.0-beta-49-g1c623cb.sxb\n')
	fp.write('\tpkg_parser = cdma-11.1.0-beta-49-g1c623cb.tar.gz\n')	
		
		
		
	

def default_stuff(argv):
#	if (os.stat('dagjobsfull.cfg').st_size!=0):
#			return os.stat('dagjobsfull.cfg').st_size==0
        print argv	
	start_date=argv[1]
	end_date=argv[2]
	carrier=argv[4]
	num_groups=100 # or in future argv[3]
	
	######################################### Common Variables ##################################
	fp = open('dagjobsfull.cfg','w')
	fp.write('carrier = %s\n' % carrier)
	switch_list(fp)
	fp.write('mega_base_url = ftp://10.255.3.20\n')
		
	fp.write('timezone = '+'America/%s\n' % argv[3])
	fp.write('num_groups = '+'%d\n' % num_groups)
	if carrier.lower() == 'verizon':
		fp.write('start_date = %s\n' % (date_converter(int(argv[1]),-1))) # One month back
		fp.write('end_date = %s\n'  %  (date_converter(int(argv[2]), 1))) # one month ahead
	else:	
		# for sprint portion should be here
		fp.write('start_date = %d\n' % int(start_date))
	        fp.write('end_date = %d\n'  % int(end_date))

	fp.write('hw_timezone = %s\n' % time_utc(argv[3]))
	fp.write('default_tech = pcmd\n')
	######################################## Files ###########################################
	fp.write('\n\n\n')	
	fp.write('block_id_file = %s\n' % ask('csv file absolute path'))
	fp.write('map_pickle = %s\n' % ask('map pickle file path'))
	fp.write('custom_zone_id_bitmap = %s\n' % ask('custom tiff image path'))
	fp.write('block_id_bitmap = %s\n' % ask('blockid tiff image path'))
	######################################## Directories ####################################
	fp.write('\n\n\n')
	fp.write('legacy_data_dir = %s\n' % ask('PDE data path'))
	fp.write('data_dir = %s\n' % ask('Output path'))
	if carrier.lower()=='sprint':
		fp.write('optout_dir = rsync:///mnt/glusterfs/od/httpd/optout/virginoptout/\n')
	elif carrier.lower()=='ibm':
		fp.write('optout_dir = rsync:///mnt/ibmlun2/virginoptout/\n')
	else:	
		print "Verizon study , so no opt out file"	

	######################################## Miscellaneous ##################################
	fp.write('\n\n\n')
	fp.write('max_disk = 999999999\n'+'retry = 1\n'+'pkg_bashreduce = bashreduce-v1.0-2-g71fffec.sxb\n')
	fp.write('declare_capacity = 1\n'+'max_cpus = 23\n')
	fp.write('legacy_header = %s\n' % header(carrier))
	fp.write('work_base_dir = work\n' + 'rank_expression = "Rank = Cpus"\n'+'timeout = 10800\n'+'adjust_epoch = 0\n'+'notify_user = ops@airsage.com\n') 
	question=ask('Points or Trips?\n')
	if question=='Trips':
		print "Nothing for now"
#		customer_matrix(start_date,end_date,fp)
		airsage_default(start_date,end_date,argv[3],fp)
		points=False
	elif (question=='Points'):
		points=True
	else:
		points=True
	#fp.close()
	if points==True:
		subprocess.call(['./activity_points.sh'])
	penetration(start_date,end_date,carrier,fp)
	dagjobs(fp)
	fp.close()
#	display(fp)

if __name__ == '__main__':
	if len(sys.argv) != 5:
        	print('usage: <./vzw_newformat.py>   <start_date> <end_date> <time/zone(ex. Chicago> <sprint/verizon/ibm')
        	sys.exit(1)
	default_stuff(sys.argv)
		
