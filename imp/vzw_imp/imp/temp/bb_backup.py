import sys
import os
import subprocess
import multiprocessing
import time
#Filename is the first argument
# days_list=qx(["python","testing_date_modified.py",start_date,end_date,each_matrix])

"""
def bb_sync(filename):
	fp = open(filename)
	for line in fp:
		line = line.strip().split('\t')
		print len(line)
		val=subprocess.call(['./bb_testing.sh',line[0],line[1],line[2],line[3],line[4],line[5],line[6]])	



if __name__=='__main__':
	filename=sys.argv[1]
	fp = open(filename)
	for line in fp:
		p = multiprocessing.Process(target=worker, args=line)
	#bb_sync(filename)
"""

def work(line):
	print line
        line = line.strip().split('\t')
        print len(line)
        val=subprocess.call(['./bb_testing.sh',line[0],line[1],line[2],line[3],line[4],line[5],line[6]])



"""
def bb_sync(filename):
        fp = open(filename)
        for line in fp:
                line = line.strip().split('\t')
                print len(line)
                val=subprocess.call(['./bb_testing.sh',line[0],line[1],line[2],line[3],line[4],line[5],line[6]])        
"""

if __name__=='__main__':
        jobs=list()
        filename=sys.argv[1]
        fp = open(filename)
        for line in fp:
                p = multiprocessing.Process(target=work, args=(line,))
                jobs.append(p)
		p.start()
		time.sleep(1)


