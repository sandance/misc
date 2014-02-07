#!/usr/bin/python

import datetime

import sys
import time 
from time import strptime

#Put your date here

start_date=sys.argv[1]
end_date=sys.argv[2]
matrix=sys.argv[3]
# start dates
start_year=int(start_date[0:4])
start_month=int(start_date[4:6])
start_day=int(start_date[6:])


# end dates 

end_month=int(end_date[4:6])
end_day=int(end_date[6:])

startdate=datetime.date(start_year,start_month,start_day)
enddate=datetime.date(start_year,end_month,end_day)

mDay,tuDay,wDay,thDay,fDay,saDay,suDay=list(),list(),list(),list(),list(),list(),list()
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
"""
print "All Monday  are"	
print " ".join(str(v) for v in mDay) 
print "\n"

print "All Tuesday  are"
print " ".join(str(v) for v in tuDay)
print "\n"

print "All Wedday  are"
print " ".join(str(v) for v in wDay)
print "\n"

print "All thuday  are"
print " ".join(str(v) for v in thDay)
print "\n"

print "All Friday  are"
print " ".join(str(v) for v in fDay)
print "\n"

"""
merge=list()

#Extension 
print "Tus Wed Thu"
merge.extend(tuDay)
merge.extend(wDay)
merge.extend(thDay)
merge.sort()
#	return merge		
print "Sat Sun"
satsun=[]
satsun.extend(saDay)
satsun.extend(suDay)
satsun.sort()
print " ".join(str(v) for v in satsun)
print "\n"

print "Total weekdays Mon Tue Wed Thu Fri\n"
total =[]
total.extend(mDay)
total.extend(merge)
total.extend(fDay)
total.sort()
print " ".join(str(v) for v in total)

"""
if (matrix=='airsageWD'):
	return merge
elif (matrix=='airsageWE'):
	return satsun
elif (matrix=='airsageHW'):
	return total
"""


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
