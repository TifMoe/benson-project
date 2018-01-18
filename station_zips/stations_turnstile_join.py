import pandas as pd

turnstiles = pd.read_pickle('stiles/cleaned_turnstile_data2.pkl')
turnstiles.station.unique()

locations = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/StationEntrances.csv')
locations.Station_Name.unique()

locations.to_csv('station_locations.csv', index=False)