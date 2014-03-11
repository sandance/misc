#!/usr/bin/python

import sys
import os
import gzip


fp=gzip.open(sys.argv[1])
subs = set()

for line in fp:
    line = line.strip().split(',')
    if line[0] == "sub1":
        continue
    if len(line) <5:
        continue
    subscriber_id = line[5]
    subs.add(subscriber_id)
print len(subs)
sys.exit()
