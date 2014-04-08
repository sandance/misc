import datetime
import calendar
import sys

def add_month(sourcedate,months):
	month = sourcedate.month -1 + months
	year  = sourcedate.year + month /12
	month = month %12 +1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	date =datetime.date(year,month,day)
	date =date.strftime('%Y%m%d')
	return date

#print add_month(datetime.date(2013,2,1),-1)


