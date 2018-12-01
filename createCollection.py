import boto3

# for AWS configuration
aws_id='XXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
collectionId='Family'
#maxResults=2


client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)

#Create a collection
print('Creating collection:' + collectionId)
response=client.create_collection(CollectionId=collectionId)
print('Collection ARN: ' + response['CollectionArn'])
print('Status code: ' + str(response['StatusCode']))
print('Done...')

