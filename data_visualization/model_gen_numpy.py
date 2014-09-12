import os
import sys
import argparse
import xlsxwriter
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import pylab as P

data = list()


def load_data(import_file):
	numFeat = len(open(import_file).readline().split(','))
	
	dataMat=list()
	fp = open(import_file)
	for line in fp.readlines():
		#lineArr= []
		curLine = line.strip().split(',')
		for i in range(numFeat):
			if i==5:
				dataMat.append(float(curLine[i]))
			else:
				continue
			
	return dataMat




def import_data(import_file):
	''' Imports data from import file '''
	with open(import_file,'r') as f:
		for line in f:
			fields = line.strip().split(",")
			data.append(list([f.strip()  for f in fields]))
	return data

def write_data(data):
	''' Write data into xlsx file '''
	#from xlwt import Workbook
	book = xlsxwriter.Workbook("test.xlsx")
	sheet1 = book.add_worksheet()
	bold   = book.add_format({'bold': True})
	format1 = book.add_format({'bg_color': '#FF0000',
                               'font_color': '#000000'})
	format2 = book.add_format({'bg_color': '#008000',
                               'font_color': '#000000'})
	


	sheet1.write('A1','Switch',bold)
	sheet1.write('B1','Tech',bold)
	sheet1.write('C1','Input_record',bold)
	sheet1.write('D1','Day',bold)
	sheet1.write('E1','Zero_counts',bold)
	sheet1.write('F1','percent',bold)
	
	row =1 

	for line in data:
		col=0
		for datum in line:
		#	print datum
			if col < 4:
				sheet1.write(row,col,datum)
			if col >= 4:
				sheet1.write_number(row,col,(round(float(datum),2)))
			col +=1
		row +=1
		# We have hard limit here of 65535 rows , that all we can save on spreadsheet
		if row > 65535:
			print >> sys.stderr, "Hit limit of excel shpeadsheet"
			break
	#book.save("model_spreadsheet.xls")
	end_limit='F'+str(row)
#	print end_limit
	sheet1.conditional_format('F2:'+end_limit,{'type': 'cell',
                                         'criteria': '>=',
                                         'value': 30.00,
                                         'format': format2})
	
	sheet1.conditional_format('F2:'+end_limit,{'type': 'cell',
                                         'criteria': '<',
                                         'value': 30.00,
                                         'format': format1})
	book.close()	
	
	



if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", dest="import_file", required=True, help="Path with ccc txt file")
	args = parser.parse_args()

	if args.import_file is None:
		print >> sys.stderr, "You must specify path to import from"
		sys.exit(1)

	#verify given path is a accessible file
	if not os.path.isfile(args.import_file):
		print >> sys.stderr , "Given path is not a file: %s" % args.import_file
		sys.exit(1)
	# read from file
	data = import_data(args.import_file)
	write_data(data)
	numpy_data = load_data(args.import_file)
	final_data  = mat(numpy_data)
	mu = mean(final_data)
	sigma = np.std(final_data)
	
	#print mu,sigma
	#hist,bin_edges = np.histogram(final_data,bins = range(5))
	#plt.bar(bin_edges[:-1],hist,width=0.5)
	#plt.xlim(min(bin_edges),max(bin_edges))
	#plt.show()
	ax = plt.gca()
	ax.hist(final_data.T,final_data)
	ax.set_xlabel('Percent')
	ax.set_ylabel('No of Switches')
	plt.show()	
