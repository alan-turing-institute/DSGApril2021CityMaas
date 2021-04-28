import sys
import csv
import rasterio
from rasterio.warp import transform
from rasterio.crs import CRS
import rasterio.transform
import json



def get_elevation(lat_lon, IMAGE_PATH):
    WGS84 = CRS.from_epsg(4326)
    epsg_27700 = CRS.from_epsg(27700)
    image = rasterio.open(IMAGE_PATH)
    results = []

    lat = lat_lon[0]
    lon = lat_lon[1]
    new_coo = transform(WGS84, epsg_27700, xs=[lon], ys=[lat])
    vals = image.sample(((new_coo[0][0], new_coo[1][0]),))
    for val in vals:
        results.append({"lat": lat, "lon": lon, "elevation": val[0]})
    return results
