from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, WebSocket, HTTPException, Response
import io
import os
from typing import Optional

from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags

import asyncio
import websockets
#TODO figure out how to get websocket working


#Declare FastAPI App
app = FastAPI()

#Create the connection manager (this is for one client, different manager for multiple)
class Manager:
    def __init__(self) -> None:
        self.active_connection: WebSocket = None

    async def connect(self, websocket: WebSocket):
        self.active_connection = websocket
    
    async def disconnect(self, websocket: WebSocket):
        await self.active_connection.close()
        self.active_connection = None
        
    async def sendImgData(self, flight_id, img_id):
        if self.active_connection == None:
            raise HTTPException(status_code=400, message="No connection active")
        data = {"flight_id":flight_id,"img_id":img_id}

        await self.active_connection.send_json(data)
    
    

#Declare Minio Server
client = Minio(
    "db:9000",
    
    # access_key=os.environ.get(MINIO_ROOT_USER),
    # secret_key=os.environ.get(MINIO_ROOT_PASSWORD),
    access_key="admin",
    secret_key="arcshimmer",
    secure=False
)
bucket="images"
temp_directory="./temp_images"
# @app.get('/setFlightID/{flight_id}') TODO implement later
# async def setFlightID(flight_id):
#     '''
#     Sets the Flight ID for this flight
#     '''
#     os.environ['flightID']=str(flight_id)
#     bucket=os.environ.get('flightID')
#     checkBucket()
#     return(bucket)

manager = Manager()
@app.websocket("/ws")
async def websocket(websocket:WebSocket):
    await websocket.accept()
    await manager.connect(websocket)
    while True:
        testVar =  await websocket.receive_text()
        print(testVar)

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
    #Set the data to send to frontend
    #Upload image to database
    #Checks if the image is already in the database
    try:
        client.fget_object(bucket_name=bucket,object_name=file.filename,file_path=str(path))
        return("File Already Exists")
    #Runs if the image doesn't already exist
    except(Exception):
        new_tag = Tags(for_object=True)
        new_tag["process"]="True"
        client.fput_object(bucket_name=bucket,object_name=file.filename,file_path=str(path),tags=new_tag,metadata={"Camera-Location": loc, "Width": str(im.width), "Height": str(im.height)})
        Image.Image.close(im)
        print(path)
        
        #Send data to frontend, notifying that an image has been added
        await Manager.sendImgData(manager,flight_id=bucket,img_id=file.filename)
        return{"status":client.fget_object(bucket_name=bucket,object_name=file.filename,file_path=str(path))}

@app.get("/get_img/{img_id}")
async def getImg(img_id:str):
    img = client.get_object(bucket_name=bucket,object_name=img_id).data
    return Response(content=img,media_type="image/png")

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
