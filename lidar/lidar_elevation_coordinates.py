import sys
import csv
import rasterio
from rasterio.warp import transform
from rasterio.crs import CRS
import rasterio.transform
import json


CSV_PATH = sys.argv[1]
IMAGE_PATH = "study_area.tif"

WGS84 = CRS.from_epsg(4326)
epsg_27700 = CRS.from_epsg(27700)

point_a = [51.5094858, -0.0916676]
point_b = [51.5100532, -0.0932849]


with open(CSV_PATH, "r") as file:
    rows = list(csv.reader(file, delimiter=";"))


coords = []

for row in rows[0]:
    if not row or row == "":
        continue
    xy = [float(coord) for coord in row[1:-1].split(", ")]
    coords.append(xy)


def get_elevation(lat_lon, image):
    results = []

    lat = lat_lon[0]
    lon = lat_lon[1]
    new_coo = transform(WGS84, epsg_27700, xs=[lon], ys=[lat])
    vals = image.sample(((new_coo[0][0], new_coo[1][0]),))
    for val in vals:
        results.append({"lat": lat, "lon": lon, "elevation": val[0]})
    return results


src = rasterio.open(IMAGE_PATH)
elevations = [get_elevation(point, src) for point in coords]

with open(f'coordinates_elevation_{(CSV_PATH)}.json', 'w') as f:
    json.dump(str(elevations), f)