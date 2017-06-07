#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds'''
import os
import timeit
from random import random
import boto3

#create temporary randomised file to prevent any compression from affecting the result
RANDOMFILE = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=16M count=4 iflag=fullblock of=' + RANDOMFILE + ' &> /dev/null')

S3RES = boto3.resource('s3')

try:
    LOCFILE = open('locations.txt', 'r')
except:
    print('locations file missing')
    raise

LOCATIONS = ()
with open('locations.txt', 'r') as f:
    for line in f:
        if line.find('#') == -1:
            LOCATIONS = LOCATIONS + (line.strip('\n'),)
print(LOCATIONS)

BUCKETS = []
for location in LOCATIONS:
    newBuckname = 'ReIsuBTeST-' + str(int(random()*1000))
    BUCKETS.append(newBuckname)
    print(LOCATIONS)
    print(location)
    S3RES.create_bucket(
        Bucket=newBuckname, CreateBucketConfiguration={'LocationConstraint': location})
    # S3RES.delete_bucket(
    #     Bucket=newBuckname)
os.system('rm -rf ' + RANDOMFILE)
