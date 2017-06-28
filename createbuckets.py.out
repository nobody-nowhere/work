#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds'''
import os
import timeit
import time

from random import random
import boto3

#create temporary randomised file to prevent any compression from affecting the result
RANDOMFILE1 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=100K count=1 iflag=fullblock of=' + RANDOMFILE1 + ' &> /dev/null')

RANDOMFILE2 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=1M count=1 iflag=fullblock of=' + RANDOMFILE2 + ' &> /dev/null')

RANDOMFILE3 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=64M count=1 iflag=fullblock of=' + RANDOMFILE3 + ' &> /dev/null')

global S3RES
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
FILES = []
KEYS = []
SPEEDS = []
TIMES = []

NEWBUCKNAME = 'ReIsuBTeST-' + str(int(random()*1000))
S3RES.create_bucket(
    Bucket=NEWBUCKNAME,
    # CreateBucketConfiguration={'LocationConstraint': location})
    )
DATA = open(RANDOMFILE1, 'rb')
start = time.time()
S3RES.Bucket(NEWBUCKNAME).put_object(Key='Test1', Body=DATA)
end = time.time()

for location in LOCATIONS:
    newBuckName = 'ReIsuBTeST-' + str(int(random()*1000))
    BUCKETS.append(newBuckName)
    print(LOCATIONS)
    print(location)
    S3RES.create_bucket(
        Bucket=newBuckName,
        CreateBucketConfiguration={'LocationConstraint': location}
        )
    data = open(RANDOMFILE1, 'rb')
    start = time.time()
    S3RES.Bucket(newBuckName).put_object(Key='Test1', Body=data)
    end = time.time()
    # S3RES.delete_bucket(
    #     Bucket=newBuckname)
    # S3RES.Bucket(newBuckname).put_object(Key='Test1', Body=data)
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test1', Body=data)''', setup='''global S3RES''', number=1)
    # data = open(RANDOMFILE2, 'rb')
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test2', Body=data)''', number=1)
    # data = open(RANDOMFILE3, 'rb')
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test3', Body=data)''', number=1)

os.system('rm -rf ' + RANDOMFILE1)
os.system('rm -rf ' + RANDOMFILE2)
os.system('rm -rf ' + RANDOMFILE3)
