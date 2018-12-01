# coding: UTF-8

import boto3
import sys
import requests

# for AWS configuration
aws_id='XXXXXXXXXXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
bucket='nbcam-img'
collectionId='Family'
fileName='input.jpg'
threshold = 10
maxFaces=5

# Receive filename from Console
args = sys.argv
pictureTaken = args[1]

#Upload photo to S3
s3 = boto3.resource('s3',
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
s3.Bucket(bucket).upload_file(pictureTaken, fileName)

#Use AWS Rekognition for search faces
client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)

response = client.search_faces_by_image(CollectionId=collectionId,
                    Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                    FaceMatchThreshold=threshold,
                    MaxFaces=maxFaces)
faceMatches=response['FaceMatches']

#List matched faces
print('Matching faces')
for match in faceMatches:
    print('Name:' + match['Face']['FaceId']) 
    #print('Name:' + d[match['Face']['FaceId']]) #Look for Name from FaceID Dict
    print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    print

