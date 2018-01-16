import pandas as pd
from geopy.geocoders import Nominatim
geolocator = Nominatim()


def fetch_addresses(df):
    """
    :param df: 'Stations' dataframe with the lat/long of each station stored
        in 'GTFS Latitude' and 'GTFS Longitude' columns
    :return: A list of addresses corresponding to each row of the stations dataframe
    Note: This takes a few minutes to complete
    """
    address_list = []
    for index, row in stations.iterrows():
        address = geolocator.reverse("{},{}".format(row['GTFS Latitude'], row['GTFS Longitude']))
        address_list.append(address)

    return address_list


# Read in data
stations = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

# Fetch addresses and pull out zipcodes
addresses = fetch_addresses(stations)
zips = [i.raw['address']['postcode'] for i in addresses]

# Add zipcode column
stations['zipcode'] = zips

stations.to_csv('stations_with_zips.csv', index_label=False)


