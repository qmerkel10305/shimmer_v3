from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form
import io
import os
from typing import Optional

from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags

from dotenv import load_dotenv
load_dotenv("../.env",verbose=True) # load the .env file from the parent directory

'''
* TODO Fix reassignment of the flightID
*
'''


#Declare FastAPI App
app = FastAPI()
#Declare Minio Server
client = Minio(
    "127.0.0.1:9000",
    access_key="admin",
    secret_key="aerial12",
    secure=False
)
bucket=os.environ['flightID']
temp_directory="./temp_images"

@app.get('/setFlightID/{flight_id}')
async def setFlightID(flight_id):
    '''
    Sets the Flight ID for this flight
    '''
    os.environ['flightID']=str(flight_id)
    bucket=os.environ.get('flightID')
    checkBucket()
    return(bucket)

@app.get('/checkBucket/')
def checkBucket():
    '''
    Checks that the bucket that we are wanting to use exists, if it does not exist, it will create a bucket, will print to console the bucket being used.
    Acts both as a function called within the program before any additions are made to the bucket and as a method for the user the check the bucket they are using
    '''
    
    exists = client.bucket_exists(str(bucket))

    if not exists:
        client.make_bucket(bucket_name=bucket)
    print("Using bucket: "+bucket)
    return("Using bucket: "+bucket)
    
    
@app.post('/shimmer/')
async def create_upload_file(file: UploadFile = File(...), loc: Optional[str] = Form(None)):
    '''
    Recieves image from post request and stores it in the database
    '''
    checkBucket()
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

@app.get('/list/')
async def listImages():
    '''
    Lists all files in the active bucket
    '''
    checkBucket()
    imgs = list()
    for i in client.list_objects(bucket_name=bucket,recursive=True):
        imgs.append(i.object_name)
    imgs.sort()
    return imgs
