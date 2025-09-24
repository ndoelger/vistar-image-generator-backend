import zipfile
import os
import base64

def unzip(zip):
    images = []

    with zipfile.ZipFile(zip, "r") as z:
        for file_name in z.namelist():
            extracted_path = z.extract(file_name, "/tmp")
            images.append(extracted_path)

    return images