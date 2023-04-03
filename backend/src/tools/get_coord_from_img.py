from utils.image import get_coord_from_img
from pyexiv2.metadata import ImageMetadata
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image", required=True, type=str)
    parser.add_argument("px", required=True, type=int)
    parser.add_argument("py", required=True, type=int)
    args = parser.parse_args()

    img = ImageMetadata(args.image)
    lat, lon = get_coord_from_img(img, args.px, args.py, to_wgs84=False)
    print(f"Latitude: {lat}, Longitude: {lon}")
