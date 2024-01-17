from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form
import io
import os
from typing import Optional

from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags


#Declare FastAPI App
app = FastAPI()
#Declare Minio Server
client = Minio(
    "127.0.0.1:9000",
    access_key="admin",
    secret_key="aerial12",
    secure=False
)
bucket="images"
temp_directory="./temp_images"

#Check that "images" bucket exists
exists = client.bucket_exists(bucket)

if not exists:
    raise Exception('\"images\" bucket not found')
else:
    print("Bucket \"images\" exists")
    
    
@app.post('/shimmer/')
#Recieves image from post request and stores it in the ./Images/ directory
async def create_upload_file(file: UploadFile = File(...), loc: Optional[str] = Form(None)):
    #Delete all files in temp_images
    for old_file in os.listdir(temp_directory):
        path = os.path.join(temp_directory,old_file)
        os.remove(path)
    #Turn the coroutine into an image
    im = Image.open(io.BytesIO(await file.read()))
    path = os.path.join(temp_directory,file.filename)
    print(path)
    im.save(path)
    #Upload image to database
    #Checks if the image is already in the database
    try:
        client.fget_object(bucket_name=bucket,object_name=file.filename,file_path=str(path))
        os.remove(path)
        return("File Already Exists")
    #Runs if the image doesn't already exist
    except(Exception):
        new_tag = Tags(for_object=True)
        new_tag["process"]="True"
        client.fput_object(bucket_name=bucket,object_name=file.filename,file_path=str(path),tags=new_tag,metadata={"Camera-Location": loc, "Width": str(im.width), "Height": str(im.height)})
        Image.Image.close(im)
        print(path)
        os.remove(path)
        return{"status":client.fget_object(bucket_name=bucket,object_name=file.filename,file_path=str(path))}

#Lists all files in the "images" bucket
@app.get('/list/')
async def listImages():
    imgs = list()
    for i in client.list_objects(bucket_name=bucket,recursive=True):
        imgs.append(i.object_name)
    imgs.sort()
    return imgs

@app.get('/setFlightID/')