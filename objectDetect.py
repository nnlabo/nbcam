# coding: UTF-8

import boto3
import sys

# Receive filename from Console
args = sys.argv
fileName = args[1]

# for AWS configuration
aws_id='XXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
bucket='XXXXXXXXXXXXXX'

client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})

print('Detected labels for ' + fileName)    
for label in response['Labels']:
    print (label['Name'] + ' : ' + str(label['Confidence']))
