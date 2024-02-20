import fiona
import geopandas as gpd
import json
from shapely.geometry import Point
import pyproj

fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# Load PlanningBoundaryArea to gdf
with fiona.open("PlanningBoundaryArea.kml") as collection:
    gdf = gpd.GeoDataFrame.from_features(collection)

# Load car park locations data
with open('Car_Park_Details.json', 'r') as file:
    carparks = json.load(file)

# init crs transformer
transformer = pyproj.Transformer.from_crs(
    "EPSG:3414",  # SVY21 (Singapore)
    "EPSG:4326"   # WGS84
)

carpark_counts = [0] * len(gdf)

# Check if a location is within a pdf boundary
def update_carpark_counts(point):
    for index, row in gdf.iterrows():
        if (row['geometry'].contains(point)):
            carpark_counts[index] += 1
            return

# Loop through all car parks
for carpark in carparks["Result"]:
    if len(carpark["geometries"]) == 0:
        continue

    x, y = carpark["geometries"][0]["coordinates"].split(",")
    lon, lat = transformer.transform(float(x), float(y))
    point = Point(lat, lon)
    update_carpark_counts(point)

# Update carparks column in gdf
gdf["carparks"] = 0
for i in range(len(gdf)):
    gdf.loc[i, 'carparks'] = carpark_counts[i]

p = gdf.plot("carparks", legend=True)
p.figure.savefig("carparks.png")
