# Shimmer backend

Dependencies:
- FastAPI: `$ pip install fastapi`
- MinIO: Follow instructions under "Docker" on the MinIO website to install Minio & run `$ pip install minio`
- uvicorn: `$ pip install uvicorn`
- python-multipart: `$ pip install python-multipart`
- websockets: `$ pip install websockets`
- Docker: Install Docker Client on Windows machine
<hr/>

## Deploying

##### 1. MinIO
- Start container on docker. 

##### 2. Uvicorn
- Default*: `.$ uvicorn api:app`
- dev*: `.$ uvicorn api:app --reload`

###### Disclaimers
*Default Port is 127.0.0.1:5000 on the VM - VSCode will automatically forward that port to your machine's 127.0.0.1:5000 port
*Default Port should be used for all development, as the port forwarding is only necessary for personal windows machines

<hr/>

## API Paths
- /shimmer/ - POST image (This will be the request made by the plane)
- /list/ - list all images stored in Images bucket
<hr/>

## Commands
- /shimmer/ - `.$ curl -X POST <IP>:<PORT>/shimmer/ -H 'Content-Type:multipart/form-data' -F 'file=@<IMAGE_FILE_NAME>'`
- /list/ - `.$ curl -X GET <IP>:<PORT>/list/ `
<hr/>

## Testing Cases
- Upload Image - `curl -X POST 127.0.0.1:5000/shimmer/ -H 'Content-Type:multipart/form-data' -F 'file=@test_IMG.png'`
- Upload 5 Images - From /backend/ - `.$ python3 ./test_post.py`
- List Get Request - `curl -X GET 127.0.0.1:5000/list/`
<hr/>

## Future Development
##### Multiple Active Frontends
Possible Options:
- Change frontend to send the bucket the image is in along with the image's name in its requests
- Use FastAPI Websocket subscriptions