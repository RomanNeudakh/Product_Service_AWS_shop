import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))

from product_service_aws_shop.lambda_handlers.get_products_list_handler import getProductsListHandler
def test_getProductsListHandler():
    event = {}
    context = {}
    response = getProductsListHandler(event, context)
    
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Methods"] == "GET"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    
    products = json.loads(response["body"])
    assert isinstance(products, list)
    assert len(products) == 6
    
    expected_products = [
        {"id": 1, "name": "product id 1", "price": 100},
        {"id": 2, "name": "product id 2", "price": 110},
        {"id": 3, "name": "product id 3", "price": 120},
        {"id": 4, "name": "product id 4", "price": 130},
        {"id": 5, "name": "product id 5", "price": 140},
        {"id": 6, "name": "product id 6", "price": 150},
    ]
    
    assert products == expected_products