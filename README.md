# Shimmer V3

## Dev
This is the figma chronicaling our plan.
https://www.figma.com/file/7gw8BuD5Aw0YhyVdel2Ib8/Untitled?type=whiteboard&node-id=2%3A383&t=ohx3HofwaXslAgt3-1

<hr/>

## Deployment
1. Navigate to `/opt/arc/shimmer_new/`
2. Run `docker compose pull`
3. Run `docker compose up --build` 
    - **DO NOT** use docker compose watch, it can cause issues with the database and frontend.
4. Backend is ready to recieve images.
    - The frontend is at `localhost:80` and the database (backup way to view images) is at `localhost:9090` with credentials admin, arcshimmer
    - If you want to test that everything is running correctly, in another pane navigate to `/opt/arc/shimmer_new/backend/` and run `$ python3 test_post.py`
        - This will post 5 images to the backend, with one having metadata.
    - If for whatever reason the database is having problems, images are stored in the `/opt/arc/shimmer_new/backend/backup_images/` folder, with the same organization as in the database
5. To shutdown - Ctrl+C the docker task 

<hr/>

## Dev. Deployment
To deploy a production environment use
```shell
docker compose -f docker-compose.yml -f docker-compose-prod.yml up
```

To deploy a dev environment with hot reloading use, run
```shell
$ docker compose watch
```
in a different pane from the main Docker process. 
Be careful, as docker compose watch can cause issues with the database and frontend.
<hr/>


<b>All configurable variables are in the project roots .env folder, including username and passkey for db

## Minio Upgrade

Run
```shell
$ docker compose up --pull
```

