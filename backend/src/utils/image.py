import math
from datetime import datetime
from typing import Tuple

import cv2
import numpy as np
import pyproj
from pyexiv2.metadata import ImageMetadata
from pyproj import Transformer

from utils.camera import GOPRO_HERO_11, Camera
from utils.location import Location

WGS84 = pyproj.Proj("epsg:4326")


def get_datetime(img: ImageMetadata) -> datetime:
    """
    Gets the datetime metadata from an image

    Args:
        img (ImageMetadata): The img to get the value of

    Returns:
        datetime: The datetime of the image
    """
    img.read()
    try:
        return img["Xmp.xmp.CreateDate"].value
    except KeyError:
        return img["Exif.Photo.DateTimeOriginal"].value


def get_nadir(img: ImageMetadata) -> bool:
    """
    Get the nadir metadata from an image

    Args:
        img (ImageMetadata): The img to get the value of

    Returns:
        bool: The nadir matadata of the image
    """
    img.read()
    if img["Xmp.ncsu.gimbal.nadir"].value is None:
        if (
            img["Xmp.ncsu.gimbal.attitude.roll"].value is not None
            and img["Xmp.ncsu.gimbal.attitude.pitch"].value is not None
        ):
            # <0.5deg of error is "nadired"
            if abs(img["Xmp.ncsu.gimbal.attitude.roll"].value) < math.radians(
                0.5
            ) and abs(img["Xmp.ncsu.gimbal.attitude.pitch"].value) < math.radians(0.5):
                img["Xmp.ncsu.gimbal.nadir"] = True
            else:
                img["Xmp.ncsu.gimbal.nadir"] = False
        # Assume images with no data are nadired.
        # This is crappy, but there is nothing else to do
        else:
            img["Xmp.ncsu.gimbal.nadir"] = True
        img.write()
    return img["Xmp.ncsu.gimbal.nadir"].value


def get_latlon(img: ImageMetadata) -> Tuple[float, float]:
    """
    Get the location metadata of the image

    Args:
        img (ImageMetadata): The image to get the value of

    Returns:
        Tuple[float, float]: A Tuple representing the lat/lon of an image
    """
    img.read()
    return (
        float(img["Xmp.ncsu.GLOBAL_POSITION_INT.lat"].value) / 1e7,
        float(img["Xmp.ncsu.GLOBAL_POSITION_INT.lon"].value) / 1e7,
    )


def as_wkt(
    img: ImageMetadata,
    bounds: Tuple[Tuple[int, int], Tuple[int, int]] = None,
    extended=True,
) -> str:
    """
    Get the image as a WKT string representation, used to query the POSTGIS database.

    Args:
        img (ImageMetadata): The image to convert
        bounds (Tuple[Tuple[int, int], Tuple[int, int]], optional): A Tuple representing bounds to identify. Defaults to None.
        extended (bool, optional): Add the SRID to the query. Defaults to True.

    Returns:
        str: The wkt string representation
    """
    img.read()
    if bounds:
        xmin, ymin = bounds[0]
        xmax, ymax = bounds[1]
    else:
        xmin, ymin = 0, 0
        xmax, ymax = img.dimensions[0], img.dimensions[1]

    corners = (
        get_coord_from_img(img, xmin, ymin, to_wgs84=False),
        get_coord_from_img(img, xmax, 0, to_wgs84=False),
        get_coord_from_img(img, xmax, ymax, to_wgs84=False),
        get_coord_from_img(img, 0, ymax, to_wgs84=False),
    )

    wkt = f"POLYGON(({corners[0][0]} {corners[0][1]}, {corners[1][0]} {corners[1][1]}, {corners[2][0]} {corners[2][1]}, {corners[3][0]} {corners[3][1]}, {corners[0][0]} {corners[0][1]}))"

    if extended:
        wkt = f"SRID={Location.get_location(*get_latlon(img)).srid};" + wkt

    return wkt


def get_coord_from_img(
    img: ImageMetadata,
    x: int = None,
    y: int = None,
    undistort: bool = True,
    to_wgs84: bool = True,
    camera: Camera = GOPRO_HERO_11,
) -> Tuple[float, float]:
    """
    Get coordinates from an image

    Args:
        img (ImageMetadata): The image to get coordinates from
        x (int, optional): The X coordinate to convert. Defaults to None.
        y (int, optional): The Y coordinate to convert. Defaults to None.
        undistort (bool, optional): Boolean to undistort using opencv. Defaults to True.
        to_wgs84 (bool, optional): Convert coordinates to lat/lon using wgs84. Defaults to True.
        camera (Camera, optional): The Camera the image was taken with. Defaults to LUCID_PHOENIX_12MM.

    Raises:
        AttributeError: X and Y must both be set of unset

    Returns:
        Tuple[float, float]: Tuple representing either (easting, northing) or (lat, lon), depending on to_wgs84
    """
    img.read()
    lat, lon = get_latlon(img)
    loc = Location.get_location(lat, lon)
    t = Transformer.from_proj(WGS84, loc.projection)

    if x is None and y is None:
        if to_wgs84:
            return lat, lon
        else:
            return t.transform(lon, lat)
    elif x is None or y is None:
        raise AttributeError("X and Y must both be set or unset.")
    else:
        # Use OpenCV undistortion algorithm to adjust x/y for distortion
        if (
            undistort
            and camera.camera_matrix is not None
            and camera.distortion_coefficients is not None
        ):
            undistorted = cv2.undistortPoints(
                np.array([[[x, y]]], dtype=np.float32),
                camera.camera_matrix,
                camera.distortion_coefficients,
                P=camera.camera_matrix,
            )
            x, y = undistorted[0, 0]

        # Coord in defined UTM coordinate system
        center_coord = t.transform(lon, lat)

        center = (img.dimensions[0] / 2, img.dimensions[1] / 2)
        width_m = (
            2
            * float(img["Xmp.ncsu.GLOBAL_POSITION_INT.relative_alt"].value)
            / 1e3
            * math.tan(math.radians(camera.hfov / 2))
        )
        height_m = (
            2
            * float(img["Xmp.ncsu.GLOBAL_POSITION_INT.relative_alt"].value)
            / 1e3
            * math.tan(math.radians(camera.vfov / 2))
        )
        width_m_per_px = width_m / img.dimensions[0]
        height_m_per_px = height_m / img.dimensions[1]

        # Distance from center, converted from pixels to meters
        delta_x = (x - center[0]) * width_m_per_px
        delta_y = (y - center[1]) * height_m_per_px

        dist = math.sqrt(delta_x**2 + delta_y**2)
        angle_from_x = math.atan2(delta_y, delta_x)

        if img["Xmp.ncsu.VFR_HUD.heading"].value is not None:
            heading = float(img["Xmp.ncsu.VFR_HUD.heading"].value) / 1e2
        else:
            heading = float(img["Xmp.ncsu.GLOBAL_POSITION_INT.heading"].value)

        angle_from_N = heading - math.pi / 2 + angle_from_x

        # If orientation is opposite from the derivation, simply add 180deg
        angle_from_N += math.pi

        north_offset = dist * math.cos(angle_from_N)
        east_offset = dist * math.sin(angle_from_N)

        easting = center_coord[0] + east_offset
        northing = center_coord[1] + north_offset

        if to_wgs84:
            # Project UTM back to WGS84 for result
            res_lon, res_lat = t.transform(easting, northing)
            return res_lat, res_lon
        else:
            return easting, northing
