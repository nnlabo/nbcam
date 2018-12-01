# coding: UTF-8

import boto3
import sys
import requests
import pygame.mixer
import time
import subprocess

# for AWS configuration
aws_id='XXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
aws_region='ap-northeast-1'
bucket='XXXXXXX'
collectionId='Family'
fileName='input.jpg'
threshold = 70
maxFaces=5

# for IFTTT
IFTTT_URL_family_found = 'https://maker.ifttt.com/trigger/OPEN_SESAME/with/key/'
IFTTT_KEY = 'XXXXXXXXXXXXXXXXXXXXX'

# For line notify
url = "https://notify-api.line.me/api/notify"
token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
headers = {"Authorization" : "Bearer "+ token}

# Registered Family Member
d = {'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA': 'BigDaddy',
     'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB': 'NOBU',
     'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX': 'A',
     'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY': 'B',
     'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ': 'C'}

# Commands for Subprocess(LED ON/OFF)
cmd_Conf = "gpio -g mode 18 out"
cmd_LED_ON = "gpio -g write 18 0"
cmd_LED_OFF = "gpio -g write 18 1"
subprocess.call(cmd_Conf.split())   # Set GPIO18 to output

# Receive filename from Motion
args = sys.argv
pictureTaken = args[1]

# Initialize Flags
Family=False
Person=False

#Start Processing
print('--------------------------------')
print('Motion Detected Start Processing')

#Turn LED ON
subprocess.call(cmd_LED_ON.split())

#Upload photo to S3
s3 = boto3.resource('s3',
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
s3.Bucket(bucket).upload_file(pictureTaken, fileName)

#Use AWS Rekognition for detect objects
client=boto3.client('rekognition', 
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_key,
        region_name=aws_region)
response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})

#List Objects and Find human
print('Detected labels for ' + fileName)    
for label in response['Labels']:
    print (label['Name'] + ' : ' + str(label['Confidence']))
    if label['Name'] == 'Person':
        Person = True
        

#Recognize Faces if Human Detected
if Person:
    print('Human Detected!')
    try:#to escape No Face Exception from AWS
        #Use Rekognition to Search Faces
        response = client.search_faces_by_image(CollectionId=collectionId,
                            Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                            FaceMatchThreshold=threshold,
                            MaxFaces=maxFaces)
        faceMatches=response['FaceMatches']

        #List matched faces
        print('Matching faces')
        for match in faceMatches:
            print('Name:' + d[match['Face']['FaceId']]) #Look for Name from FaceID Dict
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            Family=True
            print


        #Open Sesame and Send Line Notify if Family member founded
        if Family:
            print('Family Member Found!! Open SESAME!')

            # Post to IFTTT using Requests
            requests.post(IFTTT_URL_family_found + IFTTT_KEY)
        
            #Send to line notify
            message ='Family member backs to home' 
            payload = {"message" :  message}
            files = {"imageFile": open(pictureTaken, "rb")}
            r = requests.post(url ,headers = headers ,params=payload, files=files)

            #Play Okaerinasai Sound
            pygame.mixer.init(frequency = 44100) 
            pygame.mixer.music.load("okaerinasai.wav") 
            pygame.mixer.music.play(1)
            time.sleep(3)
            pygame.mixer.music.stop()

        #Just send Line Notify if its not
        else:
            print('Not a Family Member')
            #Send to line notify
            message ='Strainger Wondering' 
            payload = {"message" :  message}
            files = {"imageFile": open(pictureTaken, "rb")}
            r = requests.post(url ,headers = headers ,params=payload, files=files)

            #Play Byebye Sound
            pygame.mixer.init(frequency = 44100) 
            pygame.mixer.music.load("keikoku.mp3") 
            pygame.mixer.music.play(1)
            time.sleep(3)
            pygame.mixer.music.stop()

    #If no face detected
    except Exception:
        print('No face detected')
        pass

    #Initialize status
    Family=False
    Person = False
    subprocess.call(cmd_LED_OFF.split()) #Turn OFF LED

else:
    print('No human detected')
    subprocess.call(cmd_LED_OFF.split()) #Turn OFF LED
