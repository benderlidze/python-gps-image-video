from exif import Image

# import glob
# import shutil
import os
import json

allFiles = []


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):

    with open(image_path, "rb") as src:

        try:
            img = Image(src)
        except:
            print("ERROR!!!", image_path)
            return {"path": image_path}

    if img.has_exif:
        try:
            img.gps_longitude
            coords = (
                decimal_coords(img.gps_latitude, img.gps_latitude_ref),
                decimal_coords(img.gps_longitude, img.gps_longitude_ref),
            )
        except AttributeError:
            print("No Coordinates", image_path)
            return {"path": image_path}
    else:
        print("The Image has no EXIF information", image_path)
        return {"path": image_path}

    print(coords)
    return {
        "path": image_path,
        "lat": coords[0],
        "lng": coords[1],
    }


for currentpath, folders, files in os.walk("."):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg")):
            fileName = os.path.join(currentpath, file)
            data = image_coordinates(fileName)
            allFiles.append(data)

with open("data.json", "w") as f:
    json.dump(allFiles, f, ensure_ascii=False)
