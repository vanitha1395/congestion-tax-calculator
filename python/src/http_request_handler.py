from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import http.server
from congestion_tax_calculator import CongestionCalculator


class TaxCalculatorAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/CalculateCongestionTax":
            try:
                # parse query parameters
                content_length = int(self.headers.get('Content-Length',0))
                request_body = self.rfile.read(content_length)
                request_data = json.loads(request_body)

                #cretea a calculator instance
                calculator = CongestionCalculator(request_data["city"], request_data["vehicleId"])

                # congestion tax calculation
                congestion_tax = calculator.get_tax(request_data["travelDates"])

                print(congestion_tax)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"Congestion Tax calculated:": congestion_tax}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_error(400, str(e))

        else:
            self.send_error(404, "End point found")

# function to instantiate the server with a http-server serving endpoint

def instantiate_server(server_class=HTTPServer, handler_class=TaxCalculatorAPIHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}....")

    httpd.serve_forever()


if __name__ == "__main__":
    instantiate_server()