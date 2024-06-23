# Overview
Congestion tax calculator application is developed on java, which servers a HTTP Server providing
GET method in an endpoint '/CalculateCongestionTax', on the port 8080.

# Tools dependencies:
Java version: 22.0.1
Apache Maven 3.9.8

# Compilation commands:
$ mvn clean package

# Running the application:
$ java -jar target/congestion-tax-calculator-1.0-SNAPSHOT.jar

# Testing using curl
curl -X GET \
  http://localhost:8080/CalculateCongestionTax \
  -H 'Content-Type: application/json' \
  -d '{
    "city": "Gothenburg",
    "vehicleId": "Car",
    "travelDates": [
      "2023-06-21T07:00:00",
      "2023-06-21T07:30:00",
      "2023-06-21T08:15:00",
      "2023-06-21T15:00:00"
    ]
  }'


# Testing using postman
Import the test configuration file in the test folder into the postman web portable,
instantiate the postman desktop client in the local PC, and then
run the testcases to verify the test results.

