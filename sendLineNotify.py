# coding: UTF-8
import sys
import boto3
import requests

# For line notify
url = "https://notify-api.line.me/api/notify"
token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
headers = {"Authorization" : "Bearer "+ token}

# Receive filename from Console
args = sys.argv
fileName = args[1]

#Send to line notify
message ='Picture' 
payload = {"message" :  message}
files = {"imageFile": open(fileName, "rb")}
r = requests.post(url ,headers = headers ,params=payload, files=files)