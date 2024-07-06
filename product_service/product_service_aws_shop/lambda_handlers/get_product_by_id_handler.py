import json
import logging
import os
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def getProductByIdHandler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    logger.info(f"Context: {context}")
    try:
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('Region_name'))
        stock_table_name = os.getenv('Stock_table_name')
        product_table_name = os.getenv('Product_table_name')
        if not stock_table_name or not product_table_name:
            raise ValueError("Environment variables for table names are not set.")
        product_id = event['pathParameters']['id']
        product_table = dynamodb.Table(product_table_name)
        product_response = product_table.get_item(Key={'id': product_id})
        product = product_response.get('Item')
        if not product:
            logger.warning(f"Product with ID {product_id} not found")
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"Product with ID {product_id} not found"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Origin": "*"
                }
            }
        if 'price' in product:
            product['price'] = str(product['price'])
        stock_table = dynamodb.Table(stock_table_name)
        stock_response = stock_table.get_item(Key={'product_id': product_id})
        stock = stock_response.get('Item')
        if not stock:
            raise ValueError("Count value could not be found")
        product['count'] = str(stock['count'])
        logger.info(f"Product found: {product}")
        return {
            "statusCode": 200,
            "body": json.dumps(product),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": "*"
            }
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": "*"
            }
        }
