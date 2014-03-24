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
	vzw_header='line,sub1,dialeddigits,longitude,latitude,d2t,uncert,method,event,epoch,type_code,pr_mid,pr_cid,pr_sid,pr_donor,route_id,sub2,dummy1,dummy2,dummy3,dummy4,dummy5,dummy6,dummy7,dummy8,dummy9,dummy10'
	if version == 'vzw':
		return vzw_header



def airsage_default(start_date,end_date,t_zone,fp):
		days=list()
		fp.write('--hwmrun\n'+'zone=-f %d  %d -m zone\n'  % (int(start_date),int(end_date)))
                fp.write('--hwmrun\n'+'county=-f %d  %d -m county\n' % (int(start_date),int(end_date)))
		days_matrix=['airsageWDDP','airsageWEDP','airsageDP9class','airsageWDH','airsageWEH']
		for each_matrix in days_matrix:
			#airsageWEDP=subprocess.Popen(["python","testing_date_modified.py",start_date,end_date,'airsageWE'], stdout=PIPE)
			#days_list=subprocess.Popen(["python","testing_date_modified.py",start_date,end_date,each_matrix], stdout=PIPE)
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
                                fp.write('--admrun\n'+'%s=' % each_matrix +'America/%s' % t_zone)
                        else:
				fp.write('--tlmrun\n'+'%s=' % each_matrix +'America/%s' % t_zone)
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

def default_stuff(argv):
#	if (os.stat('dagjobsfull.cfg').st_size!=0):
#			return os.stat('dagjobsfull.cfg').st_size==0
        print argv	
	start_date=argv[1]
	end_date=argv[2]
	num_groups=100 # or in future argv[3]


	fp = open('dagjobsfull.cfg','w')
	fp.write('--anlzsubrun\n')
	fp.write('A_initial_all_subscribers=--min_avg_sight 180\n')
	fp.write('--anlzsubrun\n')
	fp.write('M_date_range=--filter %d %d --min_avg_sight 180\n' % (int(start_date),int(end_date)))
	fp.write('--anlzsubrun\n')
	fp.write('Z_adjusted_penetration=--min 3 --max auto  --filter %d  %d --min_avg_sight 180\n' % (int(start_date),int(end_date)))
	fp.write('--timezone\n'+'America/%s\n' % argv[3])
	fp.write('--hw_timezone\n'+'%s\n' % time_utc(argv[3]))
	fp.write('--timeout\n'+'43200\n'+'--data_dir\n')
	fp.write('%s\n' % ask('Output path'))
	fp.write('--legacy_data_dir\n')
	fp.write('%s\n' % ask('PDE data path'))
	fp.write('--start_date\n'+'%s\n' % (date_converter(int(argv[1]),-1))) # One month back
        fp.write('--end_date\n'+'%s\n'  %  (date_converter(int(argv[2]), 1))) # one month ahead
	fp.write('--block_id_file\n' +'%s\n' % ask('csv file absolute path'))
	fp.write('--block_id_bitmap\n'+'%s\n' % ask('blockid tiff image path'))
	fp.write('--custom_zone_id_bitmap\n'+'%s\n' % ask('custom tiff image path'))
	fp.write('--sa_params\n'+'-p 3-class\n'+'--carrier\n'+'verizon\n'+'--default_tech\n'+'pcmd\n')
	fp.write('--map_pickle\n'+'%s\n' % ask('map pickle file path'))
	fp.write('--legacy_header\n'+'%s\n' % header('vzw'))
	fp.write('--num_groups\n'+'%d\n' % num_groups)
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

	# common for both
	num_sw=int(raw_input('number of switches?\n'))
	fp.write('--switch\n')
	switches=set()
	switches=get_switches(num_sw)
	for i in switches:
		fp.write(i.strip()+'\n')	
	
	fp.close()
	if points==True:
		subprocess.call(['./activity_points.sh'])
#	display(fp)

if __name__ == '__main__':
	if len(sys.argv) != 4:
        	print('usage: <./verizon_config_writer.py>   <start_date> <end_date> <time/zone(ex. Chicago>')
        	sys.exit(1)
	default_stuff(sys.argv)
	
