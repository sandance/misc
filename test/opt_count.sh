#!/bin/bash

msc=$1
day=$2

val=`sed -n 1p work/$msc/$day/${msc}-${day}.out` 
#echo $val
#if [ -f ${msc}_opt_out.lst ]
#then
#	rm ${msc}_opt_out.lst
#	echo "$day   $val" >> ${msc}_opt_out.lst 
#else
#	echo "$day   $val" > ${msc}_opt_out.lst
#fi 
echo "$val"



