# Shimmer V3

## Dev
This is the figma chronicaling our plan.
https://www.figma.com/file/7gw8BuD5Aw0YhyVdel2Ib8/Untitled?type=whiteboard&node-id=2%3A383&t=ohx3HofwaXslAgt3-1

</hr>

## Deployment
1. Navigate to `/opt/arc/` and navigate to newshimmer or shimmerv3?  <!-- Needs fixing, I can't remember exactly what the folder is called -->
2. Run `docker compose pull`
3. Run `docker compose up -build`
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
in a different pane from the main Docker process
<hr/>


<b>All configurable variables are in the project roots .env folder, including username and passkey for db

## Minio Upgrade

Run
```shell
$ docker compose up --pull
```

