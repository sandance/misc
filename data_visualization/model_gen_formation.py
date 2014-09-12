import os
import sys
import argparse
import xlsxwriter


data = list()
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
	book = xlsxwriter.Workbook("Sheet 1")
	#book = Workbook()
	sheet1 = book.add_sheet("Sheet 1")
	col1_name = 'Switch'
	col2_name = 'Tech'
	col3_name = 'Input_record'
	col4_name = 'Day'
	col5_name = 'Zero_counts'
	col6_name = 'percent'
	
	row=0
	sheet1.write(row,0,col1_name)
	sheet1.write(row,1,col2_name)
	sheet1.write(row,2,col3_name)
	sheet1.write(row,3,col4_name)
	sheet1.write(row,4,col5_name)
	sheet1.write(row,5,col6_name)

	row +=1 

	for line in data:
		col=0
		for datum in line:
		#	print datum
			sheet1.write(row,col,datum)
			col +=1
		row +=1
		# We have hard limit here of 65535 rows , that all we can save on spreadsheet
		if row > 65535:
			print >> sys.stderr, "Hit limit of excel shpeadsheet"
			break
	book.save("model_spreadsheet.xls")
	
	
	



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
