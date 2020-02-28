from twilio.rest import Client
from datetime import datetime
import requests
import csv
import os.path
import time


examplefile = open('resort.csv')
examplereaders = csv.reader(examplefile)
outputfile = open('output.csv', 'w', newline='')
outputwriter = csv.writer(outputfile)

print('Enter Phone Number EX(18567358245): ')
phone = input()

with open('resort.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    probabilities = {}
    for line in csv_reader:
        address = line[0] + ', ' + line[1] + ', ' + line[2]

        print('Snowfall Probability for ' + address + ':')

        try:
            response = requests.get(
                'https://locationiq.org/v1/search.php?key==' + address + '&format=json')
        except Exception as e:
            print("Cannot complete request due to the following error: " + str(e))
        json = response.json()
        lat = json[0]['lat']
        lon = json[0]['lon']

        time.sleep(1)

        darksky = requests.get('https://api.darksky.net/forecast/3fae7ec346e2afd09ac33b81e6d68eab/' + lat + ',' + lon)
        dark = darksky.json()
        days = dark['daily']['data']

        prob = 0.0
        for day in days:
            try:
                precip = (float(day['precipAccumulation']))
            except KeyError:  # tries to do the thing but if we get a KeyError, do this instead of failing
                precip = 0
            prob += precip
        prob = prob / 7
        print(prob)
        probabilities[line[0]] = prob

    max_resort = ""
    max_prob = max(probabilities.values())  # dict function to get the values of the dictionary
    for key, value in probabilities.items():  # dict function to get keys and values of dictionary as tuple
        if value == max_prob:
            max_resort = key

# Your Account SID from twilio.com/console
account_sid = ""
# Your Auth Token from twilio.com/console
auth_token = ""

client = Client(account_sid, auth_token)

message = client.messages.create(
    to=phone,
    from_="+",
    body=max_resort)

print(message.sid)