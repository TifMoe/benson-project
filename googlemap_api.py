import googlemaps
import pandas as pd
from configparser import ConfigParser
import time

config = ConfigParser()
config.read('config.ini')

gmaps = googlemaps.Client(key=config.get('GoogleApiKey', 'google-api-key'))


def fetch_addresses(df):
    """
    :param df: 'Stations' dataframe with the lat/long of each station stored
        in 'GTFS Latitude' and 'GTFS Longitude' columns
    :return: A list of addresses corresponding to each row of the stations dataframe

    Note: This takes a few minutes to complete because rate limit of 50 requests per second
    https://developers.google.com/maps/documentation/geocoding/usage-limits
    """
    address_list = []

    for index, row in df.iterrows():
        if index % 45 == 0 :
            time.sleep(1)
        response = gmaps.reverse_geocode("{},{}".format(row['GTFS Latitude'], row['GTFS Longitude']))
        address_components = response[0]['address_components']
        address_list.append(address_components)

    return address_list


def fetch_zips(address_list):
    """
    :param addresses: A list of address components returned as result of GoogleAPI request
    :return: A list of zipcodes parsed from address components
    """
    zips = []
    for address in address_list:
        for component in address:
            if component['types'] == ['postal_code']:
                zips.append(component['short_name'])

    return zips


# Read in station data
stations = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

# Add new column for zipcode data
addresses = fetch_addresses(stations)
stations['zips'] = fetch_zips(addresses)

# Write new stations data to csv
stations.to_csv('stations_with_zips.csv', index_label=False)




