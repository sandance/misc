#!/usr/bin/python

import datetime

import sys
import time 
from time import strptime

mDay,tuDay,wDay,thDay,fDay,saDay,suDay=list(),list(),list(),list(),list(),list(),list()


def basic_stuff(argv):
	start_date=sys.argv[1]
	end_date=sys.argv[2]
	start_year=int(start_date[0:4])
	start_month=int(start_date[4:6])
	start_day=int(start_date[6:])
	end_month=int(end_date[4:6])
	end_day=int(end_date[6:])
	startdate=datetime.date(start_year,start_month,start_day)
	enddate=datetime.date(start_year,end_month,end_day)

#	mDay,tuDay,wDay,thDay,fDay,saDay,suDay=list(),list(),list(),list(),list(),list(),list()
	trow,wrow,throw=0,0,0
	while startdate <= enddate:
	 	bar = startdate.strftime("%A")
   		if   bar == "Monday":
			mDay.append((str(startdate)).replace('-',''))
 		elif bar == "Tuesday": 
			tuDay.append((str(startdate)).replace('-',''))
	 	elif bar == "Wednesday": 
			wDay.append((str(startdate)).replace('-',''))
	 	elif bar == "Thursday" :
			thDay.append((str(startdate)).replace('-',''))
   		elif bar == "Sunday" :
			suDay.append((str(startdate)).replace('-',''))
	 	elif bar == "Saturday" :
			saDay.append((str(startdate)).replace('-',''))
   	 	else:
			fDay.append((str(startdate)).replace('-','')) 
	 	startdate += datetime.timedelta(days=1)

def output_list(matrix):
	merge=list()
#	print "Tus Wed Thu"
	merge.extend(tuDay)
	merge.extend(wDay)
	merge.extend(thDay)
	merge.sort()
#	print "Sat Sun"
	satsun=[]
	satsun.extend(saDay)
	satsun.extend(suDay)
	satsun.sort()
#	print " ".join(str(v) for v in satsun)
#	print "\n"
#	print "Total weekdays Mon Tue Wed Thu Fri\n"
	total =[]
	total.extend(mDay)
	total.extend(merge)
	total.extend(fDay)
	total.sort()
#	print " ".join(str(v) for v in total)
	if (matrix in ('airsageWDDP','airsageDP9class','airsageWDH')):
		return merge
	elif (matrix in ('airsageWEDP','airsageWEH' )):
		return satsun
	elif (matrix in ('airsageHW')):
		return total


if __name__=='__main__':
	basic_stuff(sys.argv[:3])
	out=list()
	out=output_list(sys.argv[3])
	print out


"""
print "All Satday  are"
for i in saDay:
        print i 
print "\n"


print "All Sunday  are"
for i in suDay:
        print i 
print "\n"

"""
