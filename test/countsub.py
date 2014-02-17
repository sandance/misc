#!/usr/bin/python

import gzip
import sys
import os


subs = set()
packpath=gzip.open(sys.argv[1])


for line in packpath:
#    print sys.argv
    line = line.strip().split(',')
    if len(line) < 11:
        continue
    if line[0] == "sub1":
        continue
    subscriber_id = line[0]
    subs.add(subscriber_id)
sub_count=len(subs)
print sub_count
sys.exit()
print >> sys.stderr, 'opt out count  is done'
