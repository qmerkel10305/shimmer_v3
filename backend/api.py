from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form, WebSocket, HTTPException, Response
import io
import os
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags

import asyncio
import websockets

import datetime

global firstSend
firstSend = True

#Declare FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the connection manager (this is for one client, different manager for multiple)
class Manager:
    

    def __init__(self) -> None:
        self.noConnectionException = HTTPException(status_code=400,detail="No connection active")
        self.active_connection: WebSocket = None

    async def connect(self, websocket: WebSocket) -> None:
        self.active_connection = websocket

    async def disconnect(self, websocket: WebSocket) -> None:
        await self.active_connection.close()
        self.active_connection = None
        
    async def send_str(self, data) -> None:
        if self.active_connection == None:
            raise self.noConnectionException
        await self.active_connection.send_text(data)
        
    async def sendImgData(self, flight_id, img_id) -> None:
        if self.active_connection == None:
            raise self.noConnectionException
        data = {"type":"img","flight_id":flight_id,"img_id":img_id}

        await self.active_connection.send_json(data)
    

#Declare Minio Server

client = Minio(
    "db:" + os.environ.get("DB_API_EXTERNAL_PORT", "9000"),
    access_key=os.environ.get("MINIO_ROOT_USER", "admin"),
    secret_key=os.environ.get("MINIO_ROOT_PASSWORD", "arcshimmer"),
    # access_key="admin",
    # secret_key="arcshimmer",
    secure=False
)
temp_directory="./temp_images"
global bucket
bucket = os.environ.get("FLIGHT_ID", "testimages")
# @app.get('/setFlightID/{flight_id}') TODO implement later
# async def setFlightID(flight_id):
#     '''
#     Sets the Flight ID for this flight
#     '''
#     os.environ['flightID']=str(flight_id)
#     bucket=os.environ.get('flightID')
#     checkBucket()
#     return(bucket)

def getLatestBucket():
    '''
    Returns the most recent bucket's name
    '''
    return sorted(client.list_buckets(), key=lambda bucket: bucket.creation_date, reverse=True)[0].name



manager = Manager()
@app.websocket("/ws")
async def websocket(websocket:WebSocket):
    global bucket
    print("test3")
    await websocket.accept()
    print("test2")
    await manager.connect(websocket)
    print("test1")
    try:
        while True:
            print("truly waiting")
            data =  await manager.active_connection.receive_json()
            print(data)
            if  isinstance(data,dict):
                if 'type' in data:
                    type = data['type']
                if 'flight_id' in data:
                    if data['flight_id'] == "" or data["flight_id"] == None:
                        bucket = getLatestBucket()
                        print("---------------------------------" + bucket + "-----------------------------------")
                        for i in client.list_objects(bucket_name=bucket):
                            await manager.sendImgData(bucket,i.object_name)
                    else:
                        bucket = data['flight_id']
                        checkBucket()
                        for i in client.list_objects(bucket_name=bucket):
                            await manager.sendImgData(bucket,i.object_name)
            print("awaiting next message")
    except(RuntimeError):
        return("WS Disconnected")
            
        

@app.get('/checkBucket/')
def checkBucket() -> str:
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
async def create_upload_file(file: UploadFile = File(...), loc: Optional[str] = Form(None))  -> dict|str:
    '''
    Recieves image from post request, and stores it in the database and sends it to the frontend
    '''
    
    global firstSend
    global bucket
    if firstSend == True:
        bucket = str(datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    else:
        bucket = getLatestBucket()
    firstSend = False
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
        client.stat_object(bucket_name=bucket,object_name=file.filename)
        return("File Already Exists")
    #Runs if the image doesn't already exist
    except(S3Error):
        new_tag = Tags(for_object=True)
        new_tag["process"]="True"
        client.fput_object(bucket_name=bucket,object_name=file.filename,file_path=str(path),tags=new_tag,metadata={"Camera-Location": loc, "Width": str(im.width), "Height": str(im.height)})
        Image.Image.close(im)
        
        #Send data to frontend, notifying that an image has been added
        await manager.sendImgData(flight_id=bucket,img_id=file.filename)
        return('success')

@app.get("/get_img/{img_id}")
async def getImg(img_id:str) -> Response:
    img = client.get_object(bucket_name=bucket,object_name=img_id).data
    return Response(content=img,media_type="image")

@app.get("/get_flights")
async def getFlights() -> list:
    flights = []
    for flight in client.list_buckets():
        flights.append(flight.name)
    return (flights)

@app.get('/list/')
async def listImages() -> list:
    '''
    Lists all files in the active bucket
    '''
    checkBucket()
    imgs = list()
    for i in client.list_objects(bucket_name=bucket,recursive=True):
        imgs.append(i.object_name)
    imgs.sort()
    return imgs

# TODO Add functionality to inject metadata
# @app.get('/list/{flight_id}')
# async def listImages(flight_id:str) -> dict[str,dict]:
#     '''
#     Lists all files in the active bucket
#     '''
#     checkBucket()
#     imgs = dict()
#     for i in client.list_objects(bucket_name=flight_id,recursive=True):
#         img = client.get_object(flight_id,i.object_name)
#         img_binary = img.data
#         img_data = json.dumps(client.get_object(flight_id,i.object_name))
        
#     imgs = dict(sorted(imgs.items(), key=lambda x: x[0]))
#     return 


# Sample code to include metadata in /getimg/ and /list/
# from fastapi import Response

# @app.get("/get_img/{img_id}")
# async def getImg(img_id: str) -> Response:
#     # Retrieve the image object and metadata from MinIO
#     img_object = client.get_object(bucket_name=bucket, object_name=img_id)
#     metadata = img_object.metadata

#     # Retrieve the image data
#     img_data = img_object.data

#     # Set the appropriate headers in the response
#     headers = {
#         "Content-Type": img_object.content_type,
#         "Content-Disposition": f"inline; filename={img_id}"
#     }

#     # Include the metadata in the headers
#     for key, value in metadata.items():
#         headers[f"X-Image-Metadata-{key}"] = value

#     # Return the image data with the headers
#     return Response(content=img_data, headers=headers)