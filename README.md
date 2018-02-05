Shimmer
-------

TODO
====
- [ ] target creation / editing
  - [x] add a target
  - [ ] assign a shape and color to a target
  - [ ] be able to erase targets
  - [ ] be able to move targets
- [ ] backend image / target serving
  - [ ] be able to move through the images without reloading the page

Online image viewer for ARC

Static Web application -- RESTAPI --> backend
                                Postgres triggers--^
Python Flash socket serves image and data  

Backend
- python-flash app subscribes to postgres trigger for IMAGES table set up
Frontend
- GETs /image from  python-flask
- when postgres gets a new image it calls python flash trigger
  - [server sent event](https://www.w3schools.com/html/html5_serversentevents.asp) ?
- user does **things** to image
- user target data is given back to python-flask to store in a separate Postgres table

Pros
- via postgres trigger and server push events --> almost instant frontend updates
- images served from existing volume --> no duplicate images
- user data is saved in postgres table --> compelete selected targets history
- multiple users can be connected and recieve live updates
