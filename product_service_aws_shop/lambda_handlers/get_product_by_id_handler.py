import json
import logging

def getProductByIdHandler(event, context):
    products =  [
        {"id": 1, "name": "product id 1", "price": 100},
        {"id": 2, "name": "product id 2", "price": 110},
        {"id": 3, "name": "product id 3", "price": 120},
        {"id": 4, "name": "product id 4", "price": 130},
        {"id": 5, "name": "product id 5", "price": 140},
        {"id": 6, "name": "product id 6", "price": 150},
    ]
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        product_id = int(event['pathParameters']['id'])
    except (KeyError, TypeError, ValueError) as e:
        logger.error("Error parsing product ID: %s", e)
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid product ID"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": "*"
            }
        }
    filtered_products = list(filter(lambda product: product["id"] == product_id, products))
    product = next(iter(filtered_products), None)
    if product:
        logger.info("Product found: %s", product)
        return {
            "statusCode": 200,
            "body": json.dumps(product),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": "*"
            }
        }
    logger.warning("Product with ID %d not found", product_id)
    return {
        "statusCode": 404,
        "body": json.dumps({"message": "Product not found"}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Origin": "*"
        }
    }
