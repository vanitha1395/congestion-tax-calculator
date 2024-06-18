import http_request_handler

"""
Starting point of the http-server being instantiated
for tax calculator
"""
if __name__ == "__main__":
    print("Congestion tax calculator: instantiated")
    http_request_handler.instantiate_server()