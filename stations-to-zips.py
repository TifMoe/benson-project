import pandas as pd
from geopy.geocoders import Nominatim
import time
geolocator = Nominatim()


def fetch_zipcodes(df):
    """
    :param df: 'Stations' dataframe with the lat/long of each station stored
        in 'GTFS Latitude' and 'GTFS Longitude' columns
    :return: A list of addresses corresponding to each row of the stations dataframe

    Note: This takes a few minutes to complete because rate limit 1 request per second
    """
    address_list = []

    for index, row in df.iterrows():
        address = geolocator.reverse("{},{}".format(row['GTFS Latitude'], row['GTFS Longitude']))
        address_list.append(address)
        time.sleep(1)

    zips = [i.raw['address']['postcode'] for i in address_list]

    return zips


# Read in data
stations = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

# Add new column with zipcode containing lat/long of station
stations['zipcode'] = fetch_zipcodes(stations)

# Write stations csv to project
stations.to_csv('stations_with_zips.csv', index_label=False)

