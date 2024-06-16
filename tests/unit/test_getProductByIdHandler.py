import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))

from product_service_aws_shop.lambda_handlers.get_product_by_id_handler import getProductByIdHandler

def test_valid_product_id():
    event = {
        "pathParameters": {
            "id": "1"
        }
    }
    context = {}
    response = getProductByIdHandler(event, context)
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    product = json.loads(response["body"])
    assert product["id"] == 1
    assert product["title"] == "product id 1"
    assert product["price"] == 100

def test_invalid_product_id():
    event = {
        "pathParameters": {
            "id": "invalid id"
        }
    }
    context = {}
    response = getProductByIdHandler(event, context)
    assert response["statusCode"] == 400
    assert response["headers"]["Content-Type"] == "application/json"
    message = json.loads(response["body"])
    assert message["message"] == "Invalid product ID"

def test_product_not_found():
    event = {
        "pathParameters": {
            "id": "999"
        }
    }
    context = {}
    response = getProductByIdHandler(event, context)
    assert response["statusCode"] == 404
    assert response["headers"]["Content-Type"] == "application/json"
    message = json.loads(response["body"])
    assert message["message"] == "Product not found"