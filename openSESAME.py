# coding: UTF-8

import requests

# for IFTTT
IFTTT_URL_family_found = 'https://maker.ifttt.com/trigger/OPEN_SESAME/with/key/'
IFTTT_KEY = 'XXXXXXXXXXXXXXXXXXXXXX'


requests.post(IFTTT_URL_family_found + IFTTT_KEY)