from PIL import Image
from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    WebSocket,
    HTTPException,
    Response,
    WebSocketDisconnect,
)
import io
import os
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from minio.error import S3Error
from minio.commonconfig import Tags

import asyncio
import websockets
import requests

import json
import datetime
import pytz

global firstSend
firstSend = True


# Declare FastAPI App
app = FastAPI()

# Sets up CORS Permissions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create the connection manager (this is for one client, different manager for multiple)
class Manager:
    """
    Class to manage the websocket connection
    """

    def __init__(self) -> None:
        self.noConnectionException = HTTPException(
            status_code=400, detail="No connection active"
        )
        self.active_connection: WebSocket = None

    async def connect(self, websocket: WebSocket) -> None:
        """
        Sets the Manager's active connection to the Websocket connection
        """
        self.active_connection = websocket

    async def disconnect(self, websocket: WebSocket) -> None:
        """
        Closes the WS connection, and removes the active connection
        """
        await self.active_connection.close()
        self.active_connection = None

    async def send_str(self, data: str | int) -> None:
        """
        Sends a str over the WS connection
        """
        if self.active_connection == None:
            raise self.noConnectionException
        await self.active_connection.send_text(data)

    async def sendImgData(self, flight_id: str | int, img_id: str | int) -> None:
        """
        Sends an img's data over the WS connection
        """
        if self.active_connection == None:
            raise self.noConnectionException
        data = {"type": "img", "flight_id": flight_id, "img_id": img_id}

        await self.active_connection.send_json(data)


# Declare Minio Server
client = Minio(
    "db:" + os.environ.get("DB_API_EXTERNAL_PORT", "9000"),
    access_key=os.environ.get("MINIO_ROOT_USER", "admin"),
    secret_key=os.environ.get("MINIO_ROOT_PASSWORD", "arcshimmer"),
    secure=False,
)
# For saving only a temp copy, with no local backup
temp_directory = "./temp_images"
# Image backup directory
backup_directory = "./backup_images"
global activeFlight
activeFlight = os.environ.get("FLIGHT_ID", "testimages")

global watchingFlight
watchingFlight = ""

adlcAddress = "0.0.0.0:{0}".format(os.environ.get("ADLC_PORT", None))


def getLatestBucket():
    """
    Returns the most recent bucket's name
    """
    return sorted(
        client.list_buckets(), key=lambda bucket: bucket.creation_date, reverse=True
    )[0].name


manager = Manager()


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    """
    Websocket endpoint for the frontend to view images.\n
    The frontend will send an empty string or None if the user is looking for a live feed, and the name of a bucket if they are wanting to look at a past flight
    """
    global activeFlight
    global watchingFlight
    global firstSend
    await websocket.accept()
    await manager.connect(websocket)
    try:
        while True:
            print("truly waiting")
            data = await manager.active_connection.receive_json()
            print(data)
            if isinstance(data, dict):
                if "type" in data:
                    type = data["type"]
                if "flight_id" in data:
                    if data["flight_id"] == "" or data["flight_id"] == None:
                        # Control flow goes here if the user wants a live feed
                        try:
                            # Checks if the first image downlink of the flight has occured, if not it creates a new bucket for the flight, and tells the rest of the backend that it doesn't need to create a new bucket
                            if firstSend == True:
                                activeFlight = getTime()
                            else:
                                activeFlight = getLatestBucket()
                            firstSend = False
                            checkBucket()
                            # Because the user is wanting a live feed, sets the flight that they are watching to the currently active flight
                            watchingFlight = getLatestBucket()
                            # Sends all images currently in the latest (and watched) flight to the frontend
                            for i in client.list_objects(bucket_name=activeFlight):
                                await manager.sendImgData(activeFlight, i.object_name)
                        except IndexError:
                            # Not entirely sure why this happens, but no problems are caused by this exception block
                            pass
                    else:
                        # Flow of control goes here if the user is looking at past flights
                        watchingFlight = data["flight_id"]
                        for i in client.list_objects(bucket_name=watchingFlight):
                            await manager.sendImgData(watchingFlight, i.object_name)
            print("awaiting next message")
    except RuntimeError:
        return "WS Disconnected"
    except WebSocketDisconnect:
        return "WS Disconnected"


@app.get("/checkBucket/")
def checkBucket() -> str:
    """
    Checks that the bucket that we are wanting to use exists, if it does not exist, it will create a bucket, will print to console the bucket being used.
    Acts both as a function called within the program before any additions are made to the bucket and as a method for the user the check the bucket they are using
    """
    exists = client.bucket_exists(str(activeFlight))

    if not exists:
        client.make_bucket(bucket_name=activeFlight)
    print("Using bucket: " + activeFlight)
    return "Using bucket: " + activeFlight


@app.post("/shimmer/")
async def create_upload_file(
    file: UploadFile = File(...), metadata: Optional[str] = Form(None)
) -> str:
    """
    Recieves image from post request, and stores it in the database and sends it to the frontend 
    """
    global firstSend
    global activeFlight
    global watchingFlight
    if firstSend == True:
        activeFlight = getTime()
        print("---Creating backup folder---")
        os.mkdir(os.path.join(backup_directory, activeFlight))
        print("---Backup folder created.---")
    else:
        activeFlight = getLatestBucket()

    if watchingFlight == "":
        watchingFlight = activeFlight

    firstSend = False
    checkBucket()
    # Delete all files in temp_images
    """ Removed from test flight 1 
    for old_file in os.listdir(temp_directory):
        path = os.path.join(temp_directory,old_file)
        os.remove(path)
    """

    # Turn the coroutine into an image - We have to use client.fput because the type UploadFile is not specifically an image, so using fput makes handling the image more efficient
    im = Image.open(io.BytesIO(await file.read()))
    ''' This is for saving to a temp directory, with no local backup
    path = os.path.join(temp_directory, str(file.filename))
    '''
    path = os.path.join(backup_directory, activeFlight, str(file.filename))
    print(path)
    im.save(path)
    # Set the data to send to frontend
    # Upload image to database
    # Checks if the image is already in the database
    try:
        client.stat_object(bucket_name=activeFlight, object_name=file.filename)
        im.close()
        return "File Already Exists"
    # Runs if the image doesn't already exist
    except S3Error:
        # Verify Metadata
        if metadata is None:
            print("Invalid Metadata Supplied - Defaulting to width and height")
            metadata = {"width": str(im.width), "height": str(im.height)}
        else:
            metadata = json.loads(metadata)
            print("Valid Metadata Supplied: {0}".format(metadata))

        new_tag = Tags(for_object=True)
        new_tag["process"] = "True"

        client.fput_object(
            bucket_name=activeFlight,
            object_name=file.filename,
            file_path=str(path),
            tags=new_tag,
            metadata=metadata,
        )

        if watchingFlight == activeFlight:
            # Send data to frontend, notifying that an image has been added
            try:
                await manager.sendImgData(flight_id=activeFlight, img_id=file.filename)
                print("Image sent")
            except HTTPException:
                print("Frontend Connection Inactive")

        try:
            requests.get(adlcAddress, params=im)
        except:
            print("ADLC not connected")
        print("---------------------------------------------------")

        im.close()
        return "success"


@app.get("/get_img/{img_id}")
async def getImg(img_id: str) -> Response:
    """
    Endpoint that displays the specified img
    """
    img = client.get_object(bucket_name=watchingFlight, object_name=img_id).data
    return Response(content=img, media_type="image")


@app.get("/get_flights")
async def getFlights() -> list:
    """
    Endpoint to get a list of all created buckets
    """
    flights = []
    for flight in client.list_buckets():
        flights.append(flight.name)
    return flights


@app.get("/list/{flight_id}")
async def listImages(flight_id: str) -> list:
    """
    Lists all files in the active bucket
    """
    checkBucket()
    imgs = list()
    for i in client.list_objects(bucket_name=flight_id, recursive=True):
        imgs.append(i.object_name)
    imgs.sort()
    return imgs


@app.get("/get_img_metadata/{img}")
async def getImgMetadata(img: str) -> dict:
    """
    Endpoint to get the metadata of an image in the flight that the frontend is watching
    """
    img_info = client.stat_object(bucket_name=watchingFlight, object_name=img).metadata
    metadata = {}
    for field in img_info:
        if "x-amz-meta" in field:
            metadata[field.replace("x-amz-meta-", '')] = img_info[field]
    return metadata


def getTime() -> str:
    """
    Gets the current time for naming purposes
    """
    return str(datetime.datetime.now().astimezone(pytz.timezone('America/New_York')).strftime("%Y.%m.%d-%H.%M.%S"))