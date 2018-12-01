# coding: UTF-8

import sys
import boto3

# for AWS configuration
aws_id='XXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
bucket='XXXXXXXXXXXXXXXXXX'

# Receive filename from Console
args = sys.argv
fileName = args[1]

#Upload photo to S3
s3 = boto3.resource('s3',
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)

s3.Bucket(bucket).upload_file(fileName, fileName)


