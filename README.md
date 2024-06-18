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


### Quick test using curl
$ curl -X GET -H "Content-Type: application/json" -d '{"city":"Gothenburg","vehicleId":"car","travelDates":["2023-06-11T09:00:00","2023-06-14T18:30:00","2023-06-15T12:00:00","2023-06-23T14:00:00"]}' http://localhost:8080/CalculateCongestionTax


## Testing using PostMan
Have used Postman webclient with desktop application to run tests against the congestion tax calculator application


## Known limitations
- only available city, gothenburg, can be extended for other cities.
- The calculator doesn't choose the highest value of toll while driving within 60mins.


## Enhancements and Improvements
- Registering the IP/Port using configuration file
- Integration of python lint
- Automation of test cases using Postman
- Ability to find vehicle-type from vehicle registration number
- Invalid input handling (throwing error or negative response when invalid input provided)
- Handle vehicle and city object creation instances in a better manner
- Improve response json content
- Add more API supports apart from congestion tax calculation