#!/usr/bin/python

import json
import requests
import csv
import sys
import time
import credentials

lastUser = 45861 # Check failed_requests.txt

def geocodePostcode(userAddress, apiKey):

    url = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = dict(
        address=userAddress,
        key=apiKey
    )

    response = requests.get(url=url, params=params)

    data = json.loads(response.text)

    status = data['status']

    print status
    if status != 'OK':
        sys.exit(0)
    else:
        return data['results'][0]['geometry']['location']


with open('data/data.csv', 'r') as csvIn, open('results/geocoded_data.csv','a+') as csvOut:

    # Map the information into a dict
    reader = csv.DictReader(csvIn)
    # Get the keys and add the new ones
    inFieldnames = reader.fieldnames
    outFieldnames = inFieldnames + ['Lat', 'Lng']

    writer = csv.DictWriter(csvOut, outFieldnames)
    if lastUser == 0:
        writer.writeheader()

    for row in reader:
        # print row['user_id'], row['address_postcode']
        userPostcode = row['address_postcode']
        userId = row['user_id']

        if int(userId) > lastUser: # Assumes ascending order

            print 'Geocoding user_id ' + userId + ' with postcode ' + userPostcode + '...'

            location = geocodePostcode(userPostcode, apiKey)
            time.sleep(0.5)
            writer.writerow({'user_id': userId, 'address_postcode': userPostcode, 'Lat': location['lat'], 'Lng': location['lng']})
        else:
            print 'User ' + userId + ' already processed'


csvIn.close()
csvOut.close()

