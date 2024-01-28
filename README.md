## Dev
This is the figma chronicaling our plan.
https://www.figma.com/file/7gw8BuD5Aw0YhyVdel2Ib8/Untitled?type=whiteboard&node-id=2%3A383&t=ohx3HofwaXslAgt3-1

</hr>

## Deployment
To deploy a production environment use
```shell
docker compose -f docker-compose.yml -f docker-compose-prod.yml up
```

To deploy a dev environment with hot reloading use
```shell
$ docker compose watch
```

All configurable variables are in the project roots .env folder.

## Minio Upgrade
```shell
$ docker compose up --pull always
```
