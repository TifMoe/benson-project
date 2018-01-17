import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Import zip shape file and stations data
zip_codes = gpd.GeoDataFrame.from_file('zip_code_shape_files/ZIP_CODE_040114.shp')
stations = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

# Convert stations lat/lon to geopoint
geometry = [Point(xy) for xy in zip(stations['GTFS Longitude'], stations['GTFS Latitude'])]
crs = {'datum':'NAD83', 'init':'epsg:4326'}
stations_geo = gpd.GeoDataFrame(stations, crs=crs, geometry=geometry)
stations_geo.crs = zip_codes.crs

stations_zips = gpd.sjoin(stations_geo, zip_codes, how="inner")
print(len(stations_zips))

test_pt = stations_geo.loc[0, 'geometry']
