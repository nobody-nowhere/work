#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds'''
import os
import timeit
import time
from pprint import pprint

from random import random
import boto3

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#create temporary randomised file to prevent any compression from affecting the result
RANDOMFILE1 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=100K count=1 iflag=fullblock of=' + RANDOMFILE1 + ' &> /dev/null')

RANDOMFILE2 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=1M count=1 iflag=fullblock of=' + RANDOMFILE2 + ' &> /dev/null')

RANDOMFILE3 = '/tmp/tmpfile{}'.format(int(random()*1000))
os.system('dd if=/dev/urandom bs=10M count=1 iflag=fullblock of=' + RANDOMFILE3 + ' &> /dev/null')

S3RES = boto3.resource('s3')

try:
    LOCFILE = open('locations.txt', 'r')
except:
    print('locations file missing')
    raise

#Since us east does not require any location constraint attribute, deal with it separately
LOCATIONS = ('us-east-1', )
with open('locations.txt', 'r') as f:
    for line in f:
        if line.find('#') == -1:
            LOCATIONS = LOCATIONS + (line.strip('\n'),)
pprint(LOCATIONS)

BUCKETS = []
FILES = []

SPEEDS = []
SIZES = []
TIMES = []

#Deal with us-east-1
NEWBUCKNAME = 'reisubtest-' + str(int(random()*1000))
BUCKETS.append(NEWBUCKNAME)
S3RES.create_bucket(
    Bucket=NEWBUCKNAME,
    # CreateBucketConfiguration={'LocationConstraint': location})
    )
START = time.time()
S3RES.Bucket(NEWBUCKNAME).put_object(Key='Test1', Body=open(RANDOMFILE1, 'rb'))
END = time.time()
TIMES.append(END-START)
SIZES.append(os.stat(RANDOMFILE1).st_size)

for location in LOCATIONS:
    #Deal with the others
    if location != 'us-east-1':
        newBuckName = 'reisubtest-' + str(int(random()*1000))
        BUCKETS.append(newBuckName)
        S3RES.create_bucket(
            Bucket=newBuckName,
            CreateBucketConfiguration={'LocationConstraint': location}
            )
        start = time.time()
        S3RES.Bucket(newBuckName).put_object(Key='Test1', Body=open(RANDOMFILE1, 'rb'))
        end = time.time()
        TIMES.append(end-start)
        SIZES.append(os.stat(RANDOMFILE1).st_size)
    # S3RES.delete_bucket(
    #     Bucket=newBuckname)
    # S3RES.Bucket(newBuckname).put_object(Key='Test1', Body=data)
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test1', Body=data)''', setup='''global S3RES''', number=1)
    # data = open(RANDOMFILE2, 'rb')
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test2', Body=data)''', number=1)
    # data = open(RANDOMFILE3, 'rb')
    # timeit.timeit('''S3RES.Bucket(newBuckname).put_object(Key='Test3', Body=data)''', number=1)

i = 0
for i in range(len(TIMES)):
    SPEEDS.append(sizeof_fmt(SIZES[i] / TIMES[i]) + '/s')
pprint(SPEEDS)

for bucket in S3RES.buckets.all():
    if bucket.name.find('reisubtest') != -1:
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()

os.system('rm -rf ' + RANDOMFILE1)
os.system('rm -rf ' + RANDOMFILE2)
os.system('rm -rf ' + RANDOMFILE3)
