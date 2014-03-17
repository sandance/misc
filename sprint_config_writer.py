#!/usr/bin/python


import sys
import os
import subprocess 
from subprocess import PIPE
from subprocess import check_output as qx

def header(version):
	vzw_header='uid,tech,filename,line,sub1,sub2,dd,epoch,event,tcode,pilots,tt,cd,ot,pilot1,pilot2,pilot3,pilot4,pilot5,v_parser,kclass,serv_cid,sub_cid,optout,longitude,latitude,d2t,uncert,method,type_code,pr_donor,msc,tag,v_pde'
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
			#days_list.stdout.flush()  # cleaning the buffer
			#Popen.terminate()
			#days_list.stdin.flush()
			r=a[2:str_len-2] # trivial process, dont know how to make it nice
			for i in r.split(','):
				val=i.replace("'",'')
				days.append(val)
			#fp.write('--tlmrun\n')
			fp.write('--tlmrun\n'+'%s=' % each_matrix +'America/%s' % t_zone)
			if each_matrix  in ('airsageWDDP', 'airsaegeWDH','airsageDP9class'):
				fp.write(' -g Tue Wed Thu -f ')
			else:
				fp.write(' -g Sat Sun -f ')
			fp.write(' '.join(str(v) for v in days))
			del days[:] # delete the list 
			if 'DP' in each_matrix: # that is dap part exist 
				fp.write(' -t 0000-0600-H0:H6 0600-1000-H06:H10  1000-1500-H10:H15 1500-1900-H15:H19 1900-2400-H19:H24')
			else:
				fp.write(' -t H')
			if each_matrix  in ('airsageDP9class'):
				fp.write(' -p 9-class --subscriber2class\n')
			else:
				fp.write(' -p --subscriber2class -p 3-class\n')

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
#	fp.write('--anlzsubrun\n')
#	fp.write('M_date_range=--filter %d %d --min_avg_sight 180\n' % (int(start_date),int(end_date)))
	fp.write('--anlzsubrun\n')
	fp.write('Z_adjusted_penetration=--min 3 --max auto  --min_avg_sight 180\n')
	fp.write('--timezone\n'+'America/%s\n' % argv[3])
	fp.write('--hw_timezone\n'+'%s\n' % time_utc(argv[3]))
	fp.write('--timeout\n'+'43200\n'+'--data_dir\n')
	fp.write('%s\n' % ask('Output path'))
	fp.write('--legacy_data_dir\n')
	fp.write('%s\n' % ask('PDE data path'))
	fp.write('--mega_base_url\n'+'ftp://10.255.3.20\n')
        fp.write('--optout_dir\n'+'rsync:///mnt/glusterfs/od/httpd/optout/virginoptout/\n')
	fp.write('--start_date\n'+'%d\n' % int(start_date))
	fp.write('--end_date\n'+'%d\n'	% int(end_date))
	fp.write('--block_id_file\n' +'%s\n' % ask('csv file absolute path'))
	fp.write('--block_id_bitmap\n'+'%s\n' % ask('blockid tiff image path'))
	fp.write('--custom_zone_id_bitmap\n'+'%s\n' % ask('custom tiff image path'))
	fp.write('--sa_params\n'+'-p 3-class\n'+'--carrier\n'+'verizon\n'+'--default_tech\n'+'pcmd\n')
	fp.write('--map_pickle\n'+'%s\n' % ask('map pickle file path'))
	fp.write('--legacy_header\n'+'%s\n' % header('vzw'))
	fp.write('--num_groups\n'+'%d\n' % num_groups)
#	fp.write('--hwmrun\n'+'zone=-f %d  %d -m zone\n'  % (int(start_date),int(end_date)))  
#	fp.write('--hwmrun\n'+'county=-f %d  %d -m county\n' % (int(start_date),int(end_date)))
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
	default_stuff(sys.argv)
	
