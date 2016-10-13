#!/usr/bin/python
import csv
import time
# Requires geopy: pip install geopy
# Using Nominatim

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

## Filenames

inputFilename  = 'data/data.csv'
outputFilename = 'results/geocoded_data_geopy.csv'
errorFilename  = 'results/geocoding_error.csv'

geolocator = Nominatim(format_string="%s", country_bias="United Kingdom")

lastUser = 0  # Check failed_requests.txt

with open(inputFilename, 'r') as csvIn, \
        open(outputFilename, 'a+') as csvOut,\
        open(errorFilename, 'a+') as csvErr:

    # Map the information into a dict
    reader = csv.DictReader(csvIn)
    # Get the keys and add the new ones
    inFieldnames = reader.fieldnames
    outFieldnames = inFieldnames + ['Lat', 'Lng']

    writer = csv.DictWriter(csvOut, outFieldnames)
    writerErr = csv.DictWriter(csvErr, inFieldnames)

    if lastUser == 0:
        writer.writeheader()

    for row in reader:
        # print row['user_id'], row['address_postcode']
        userPostcode = row['address_postcode']
        userId = row['user_id']

        if int(userId) > lastUser: # Assumes ascending order

            print 'Geocoding user_id ' + userId + ' with postcode ' + userPostcode + '...'

            try:
                location = geolocator.geocode(userPostcode)
                time.sleep(1)
                writer.writerow({'user_id': userId, 'address_postcode': userPostcode, 'Lat': location.latitude, 'Lng': location.longitude})
                print "OK"
            except (GeopyError, AttributeError):
                print "Oops, " + userId + " with postcode " + userPostcode + " couldn't be geocoded"
                writerErr.writerow({'user_id': userId, 'address_postcode': userPostcode})

        else:
            print 'User ' + userId + ' already processed'


csvIn.close()
csvOut.close()
csvErr.close()

