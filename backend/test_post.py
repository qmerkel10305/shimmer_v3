import requests
import os
import json
from io import BytesIO
# Define the URL
url = "http://127.0.0.1:5000/shimmer/"

# Define the file path and metadata for the specific image
image_path = "./test_images/test_IMG.png"
metadata = (None, json.dumps({"test_key":"test_value"}).encode('utf-8'))
# Send POST requests for each image in the directory
for img in os.listdir("./test_images"):
    try:
        image_file = os.path.join("./test_images", img)
        if img == "test_IMG.png":
            print("-----------Test Metadata----------------")
            files = {
                "file": open(image_file, "rb"),
                "metadata":metadata,
            }

        else:
            print("****************************")
            files = {"file": open(image_file, "rb")}
        response = requests.post(url, files=files)
        print(response.text)
    except Exception as e:
        print(str(e))
