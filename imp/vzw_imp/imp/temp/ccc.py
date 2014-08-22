import sys
import re

def do_work(filename):
	data= []
	fp = open(filename)
	for line in fp:
		line = line.strip().split(' ')
		data.append(line)
	return data
	
def get_count(data):
	switch_check=re.compile(r"[a-zA-Z0-9_]")
        end_line = re.compile(r"[a-zA-Z]")	
	final_output = list()
	for k,i  in enumerate(data):
		if switch_check.search(i[0]) and not i[1].find('2013'):
			#print "match found"
			sw = list()
			final_output.append(i[0])
			final_output.append(i[1])
		else:
			if i[1]=='0':
				count_0 = int(i[0])
				#print "count 0 %d" % count_0
				sw.append(int(i[0]))
				final_output.append(count_0)
			elif i[1]=='error_code':
				#print "Found error code"
				final_output.append(sum(sw[:]))
				flag=1
				if 'pcmd' in final_output[0]:
					flag=2
				percent=float(sw[0]) * 100.0 / (flag * float(sum(sw[:])))
				final_output.append(round(percent,2))
				del sw[:]
			#	print "This is what is want"
			#	print i[1]
			elif len(sw) < 3  and i[1]=='502':
				sw.append(int(i[0]))
				final_output.append(sum(sw[:]))
				flag=1
                                if 'pcmd' in final_output[0]:
                                        flag=2
                                percent=float(sw[0]) * 100.0 / (flag * float(sum(sw[:])))
                                final_output.append(round(percent,2))
				del sw[:]
			else:
				sw.append(int(i[0]))
	#print final_output
	return final_output
				 			
if __name__=='__main__':
	datalist = do_work(sys.argv[1])
	final_data=get_count(datalist)
	print final_data 
	for i in range(0,len(final_data),5):
		dis=",".join(str(x) for x in final_data[i:i+5])
		print dis.strip('[]')
	# now calculate percentage

