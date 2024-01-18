# Shimmer backend

Dependencies:
- uvicorn: `$ pip install uvicorn`
- python-multipart: `$ pip install python-multipart`
- FastAPI: `$ pip install fastapi`
- dotenv: `pip install -U python-dotenv`
- Docker: Install Docker Client on Windows machine
- MinIO: Follow instructions under "Docker" on the MinIO website to install Minio & run `$ pip install minio`
- websockets: `$ pip install websockets`
<hr/>
## Deploying
##### 1. MinIO
- Start container on docker. 

##### 2. Uvicorn
- Default*: `.$ uvicorn api:app`
- dev*: `.$ uvicorn api:app --reload`

###### Disclaimers
*Default Port is 127.0.0.1:8000 on the VM - VSCode will automatically forward that port to your machine's 127.0.0.1:8000 port
*Default Port should be used for all development, as the port forwarding is only necessary for personal windows machines

<hr/>

## API Paths
- /shimmer/ - POST image (This will be the request made by the plane)
- /list/ - list all images stored in Images bucket
<hr/>

## Commands
- /shimmer/ - `.$ curl -X POST <IP>:<PORT>/shimmer/ -H 'Content-Type:multipart/form-data' -F 'file=@<IMAGE_FILE_NAME>'`
- /list/ - `.$ curl -X GET <IP>:<PORT>/list/ `

## Testing Cases
- Upload Image - `curl -X POST 127.0.0.1:8000/shimmer/ -H 'Content-Type:multipart/form-data' -F 'file=@test_IMG.png'`
- List Get Request - `curl -X GET 127.0.0.1:8000/list/`
