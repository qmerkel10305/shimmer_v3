Shimmer
-------

Online image viewer for ARC

flask-socketio

Static Web application --[socket connection] --> backend 
                                Postgres triggers --^
Python Flash socket  only serves image locaition 
NGINX serves static images 

Backend
- python-flash app subscribes to postgres trigger for IMAGES table set up
- NGINX started to serve static content from image volume
Frontend
- socket connection is established with python-flask
- when postgres gets a new image it calls python flash trigger for...
- socket to send a "new image message" with static image path on NGINX to frontend
- frontend calls NGINX for static image and displays
- user does **things** to image
- user input data is given back to python-flask to store in a separate Postgres table

Pros
- via postgres trigger and socket connection --> almost instant frontend updates
- NGINX serves images from exists volume --> no duplicate images
- user data is saved in postgres table --> compelete selected targets history
- multiple users can be connected and recieve live updates

Cons
- potientially expensive process (running NGINX with python-flask uWSGI)
- front end could be a lot of work
