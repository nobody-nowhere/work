#!/usr/bin/env python3
''' A simple script to upload a random file to Amazon S3 and also display upload speeds'''
import os
from random import random
import boto3
import timeit

s3 = boto3.client('s3')
buckets = s3.list_buckets()['Buckets']
for bucket in buckets:
    if bucket['Name'].find('ReIsuBTeST') != -1:
        s3.delete_bucket(Bucket=bucket['Name'])
