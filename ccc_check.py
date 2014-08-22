
__author__ = 'nazmul'

import sys
import os, os.path
import gzip
import lzma



''' Algorithm:
    Take the pde path from argparse command line

    Take the switch list by terminal input

    go through the files , do the counts
'''

def CCC_check(pde_path,msc,day):
        for subdir, dirs, files in os.walk(pde_path+'/'+msc+'/'+day):
                type_count = dict()
                for fs in files:
                        filepath = os.path.join(subdir,fs)
                        ext = os.path.splitext(filepath)[-1].lower() # gets the file extension

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
                return round(percent,2), switch, input_count




if __name__ == '__main__':
        print "Enter number of swithes you want ccc for"
        n = input()
        sw = list()
        for i in range(n):
                sw.append(raw_input())

        # done with all switch name
        days = list()
        print "how many days ccc you want"
        n_ccc = input()
        for i in range(n_ccc):
                days.append(raw_input().strip())

        final_output = list()
	final_output.append(['switch','day','tech','input_record_count','percentage'])
        pde_path=sys.argv[1]
        for msc in sw:
            for day in days:
                result, sw_tech, input_count = CCC_check(pde_path, msc, day)
                final_output.append([msc, day, sw_tech, input_count, result])
	for i in final_output:
		i=str(i)	
		print i.strip("[]").replace("'","")

