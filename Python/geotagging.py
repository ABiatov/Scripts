#!/usr/bin/env python
# source: http://stackoverflow.com/questions/453395/what-is-the-best-way-to-geotag-jpeg-images-with-python?lq=1
import pyexiv2
import fractions
from PIL import Image
from PIL.ExifTags import TAGS
import sys

def to_deg(value, loc):
        if value < 0:
            loc_value = loc[0]
        elif value > 0:
            loc_value = loc[1]
        else:
            loc_value = ""
        abs_value = abs(value)
        deg =  int(abs_value)
        t1 = (abs_value-deg)*60
        min = int(t1)
        sec = round((t1 - min)* 60, 5)
        return (deg, min, sec, loc_value)    

def set_gps_location(file_name, lat, lng):
    """Adds GPS position as EXIF metadata

    Keyword arguments:
    file_name -- image file
    lat -- latitude (as float)
    lng -- longitude (as float)

    """
    lat_deg = to_deg(lat, ["S", "N"])
    lng_deg = to_deg(lng, ["W", "E"])

    print lat_deg
    print lng_deg

    # convert decimal coordinates into degrees, munutes and seconds
    exiv_lat = (pyexiv2.Rational(lat_deg[0]*60+lat_deg[1],60),pyexiv2.Rational(lat_deg[2]*100,6000), pyexiv2.Rational(0, 1))
    exiv_lng = (pyexiv2.Rational(lng_deg[0]*60+lng_deg[1],60),pyexiv2.Rational(lng_deg[2]*100,6000), pyexiv2.Rational(0, 1))
    metadata = pyexiv2.ImageMetadata(file_name)
    metadata.read()

##    exif_keys = metadata.exif_keys

    metadata["Exif.GPSInfo.GPSLatitude"] = exiv_lat
    metadata["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
    metadata["Exif.GPSInfo.GPSLongitude"] = exiv_lng
    metadata["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
    metadata["Exif.Image.GPSTag"] = 654
    metadata["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
    metadata["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'

    metadata.write()
