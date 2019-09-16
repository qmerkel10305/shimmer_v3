# Shimmer Target Viewer
The shimmer target viewer is a node based web-app using Angular2 and flask.
Software requirements:
* Node.js
* Provisioned vms
* Angularjs (installable running `npm install -g @angular/cli`)

## Building the Frontend
To build the frontend, navigate to `./frontend` and run `ng build`
## Running the Frontend
To run the frontend, navigate to `./frontend` and run `ng serve`
Once this is complete, shimmer can accessed by going `localhost:4200`. This can be done on either the groundpc vm or your own machine.
## Running the Backend
To start up the backend run `python3 ./run.py` on the groundpc vm. 

NOTE: This will not work on your local machine since it utilizes the ARC module. Follow the instructions in codelabs for how to simulate a flight.