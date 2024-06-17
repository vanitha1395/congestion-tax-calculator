import pytest
from http_request import send_http_request
import json

@pytest.fixture
def read_test_data():
    with open("test_data/entries.json", r) as file:
        data = json.load(file)
    return data

def test_send_http_request_get(sample_data):
    url = "http://localhost:3000/CalculateCongestionTax/"
    method = "GET"
