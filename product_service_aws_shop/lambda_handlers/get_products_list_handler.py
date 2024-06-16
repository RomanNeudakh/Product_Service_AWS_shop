import json

def getProductsListHandler(event, context):
    products =  [
        {"id": 1, "name": "product id 1", "price": 100},
        {"id": 2, "name": "product id 2", "price": 110},
        {"id": 3, "name": "product id 3", "price": 120},
        {"id": 4, "name": "product id 4", "price": 130},
        {"id": 5, "name": "product id 5", "price": 140},
        {"id": 6, "name": "product id 6", "price": 150},
    ]
    return {
        "statusCode": 200,
        "body": json.dumps(products),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Origin": "*"
        }
    }