__author__ = 'nazmul'


import sys
import os, os.path
import gzip
import lzma
import argparse


def CCC_check(pde_path,msc,day):
        for subdir, dirs, files in os.walk(pde_path+'/'+msc+'/'+day):
                type_count = dict()
                for fs in files:
                        filepath = os.path.join(subdir,fs)
                        ext = os.path.splitext(filepath)[-1].lower() # gets the file extension
			#print "processing %s" % filepath
                        if ext == ".gz":
                            fp = gzip.open(filepath, "rb")
                        elif ext == ".xz":
                            fp = lzma.LZMAFile(filepath)
                        else:
                            continue

                        for record in fp:
                            val = record.strip().split(',')[10]
                            if val not in type_count:
                                type_count[val] = 1
                            else:
                                type_count[val] += 1


                # count is done for all switches , now get the percentage
                input_count = float(sum(type_count.values()))

                if 'pcmd' in msc:
                        flag = 2
                        switch='lucent'
                        percent = float(type_count['0']) * 100.0 / (flag * float(sum(type_count.values())))
                else:
                        # nortel or motorolla
                        flag = 1
                        if 'csl' in msc:
                            switch='nortel'
                        else:
                            switch='motorola'
                        percent = float(type_count['0']) * 100.0 / (flag * float(sum(type_count.values())))
                return round(percent, 2), switch, input_count




if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input", dest="filename", required=True, help="Input file with switch and day", metavar="FILE")
	parser.add_argument("-p", "--path", dest="pde_path", required=True, help="path for pde data")

        args = parser.parse_args()

        fp = open(args.filename)
        sw = set()
        days = list()
        for i in fp:
            line = i.strip().split(',')
            sw.add(str(line[0]))
            days.append(line[1])
	    #print line[0], line[1]

        final_output = list()
	final_output.append(['switch','day','tech','input_record_count','percentage'])
        pde_path=args.pde_path
        for msc in sw:
            for day in days:
                result, sw_tech, input_count = CCC_check(pde_path, msc, day)
                final_output.append([msc, day, sw_tech, input_count, result])
	#print final_output
	for i in final_output:
		i=str(i)
		print i.strip("[]").replace("'","")
