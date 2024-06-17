# congestion-tax-calculator
## Overview
This project focuses on calculating the congestion taxes for vehicles.
This applicaiton is built using python, and provides an HTTP endpoint to calculate congesstion tax vehicle based on json input. 

## Tools and plugins used


## Project structure
- Folder `src` contains the source code
- Folder `tests` contains test cases and sample/test data.


## How to execute the program

### building docker(inside src folder)
$ docker build -t congestiontaxapp .

### Check for the docker image created by using
$ docker images

### Running the application within docker
$ docker run -p 8080:8080 congestiontaxapp


## Known limitations
- only available city, gothenburg, can be extended for other cities.


## Enhancements and Improvements
- Ability to find vehicle-type from vehicle registration number