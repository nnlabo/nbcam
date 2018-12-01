# coding: UTF-8
import sys
import boto3

# for AWS configuration
aws_id='XXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
bucket='XXXXXXXXXXXX'
collectionId='Family'

# Receive filename from Console
args = sys.argv
fileName = args[1]

#Upload photo to S3
s3 = boto3.resource('s3',
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
s3.Bucket(bucket).upload_file(fileName, fileName)

# Regist to rekogniton index_Face
client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
response=client.index_faces(CollectionId=collectionId,
        Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
        ExternalImageId=fileName,
        DetectionAttributes=['ALL'])

print ('Faces in ' + fileName)
for faceRecord in response['FaceRecords']:
        print (faceRecord['Face']['FaceId'])


