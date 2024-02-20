import geopandas
from geodatasets import get_path

path_to_data = get_path("nybb")
gdf = geopandas.read_file(path_to_data)

gdf.to_file("my_file.geojson", driver="GeoJSON")


transformer = pyproj.Transformer.from_crs(
    "EPSG:3414",  # SVY21 (Singapore)
    "EPSG:4326"   # WGS84
)
