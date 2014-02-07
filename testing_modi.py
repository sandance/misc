#!/usr/bin/python
import datetime
import sys
import time 
from time import strptime

#Put your date here


start_date=sys.argv[2]
end_date=sys.argv[2]

# start dates
start_year=start_date[1:4]
start_month=start_date[5:6]
start_day=start_date[6:]


# end dates 

end_month=end_date[5:6]
end_year=end_date[6:]

print "start date %s %s %s" % start_year,start_month,start_day 

#startdate=datetime.date(2013,3,21)
#enddate=datetime.date(2013,6,21)



"""

mDay,tuDay,wDay,thDay,fDay,saDay,suDay=[],[],[],[],[],[],[]
trow,wrow,throw=0,0,0
while startdate <= enddate:
	 bar = startdate.strftime("%A")	
#  	 startdate += datetime.timedelta(days=1)	
   	 if   bar == "Monday": 
		mDay.append(str(startdate))
 	 elif bar == "Tuesday": 
		 tuDay.append(str(startdate))
                 trow = trow +1
	 elif bar == "Wednesday": 
		 wDay.append(str(startdate))
                 wrow = wrow +1
	 elif bar == "Thursday" :
		thDay.append(str(startdate))
                throw = throw +1
   	 elif bar == "Sunday" :
		suDay.append(str(startdate))
	 elif bar == "Saturday" :
		saDay.append(str(startdate))
   	 else:
		fDay.append(str(startdate)) 
	 startdate += datetime.timedelta(days=1)
	

print "All Monday  are"
for i in mDay:
	print i 
print "\n"


print "All Tuesday  are"
for i in tuDay:
        print i 
print "\n"


print "All Wedday  are"
for i in wDay:
        print i 
print "\n"

print "All thuday  are"
for i in thDay:
        print i 
print "\n"



print "All Friday  are"
for i in fDay:
        print i 
print "\n"

#Extension 

print "Tus Wed Thu"
merge=[]
merge.extend(tuDay)
merge.extend(wDay)
merge.extend(thDay)

for i in merge:
	print i.strip()

print "\n\n"	
print "Sat Sun"
satsun=[]
satsun.extend(saDay)
satsun.extend(suDay)

for i in satsun:
	print i.strip() 



print "Total weekdays Mon Tue Wed Thu Fri\n"

total =[]
total.extend(mDay)
total.extend(merge)
total.extend(fDay)

for i in total:
	print i.strip()



print "All Satday  are"
for i in saDay:
        print i 
print "\n"


print "All Sunday  are"
for i in suDay:
        print i 
print "\n"

"""
