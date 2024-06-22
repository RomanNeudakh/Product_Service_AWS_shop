from decimal import Decimal
import json
import logging
import os
import uuid
import boto3

def createProductHandler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('Region_name'))
        stock_table_name = os.getenv('Stock_table_name')
        product_table_name = os.getenv('Product_table_name')
        if not stock_table_name or not product_table_name:
            raise ValueError("Environment variables for table names are not set.")
        stock_table = dynamodb.Table(stock_table_name)
        product_table = dynamodb.Table(product_table_name)
        body = json.loads(event['body'])
        product_id = str(uuid.uuid4())
        title = body['title']
        description = body.get('description', '')
        price = body['price']
        product = {
            'id': product_id,
            'title': title,
            'description': description,
            'price': Decimal(str(price))
        }
        product_table.put_item(Item=product)
        logger.info(f"Product created: {product}")
        count = body['count']
        stock = {
            'product_id': product_id,
            'count': Decimal(str(count))
        }
        stock_table.put_item(Item=stock) 
        logger.info(f"Product was added: {product}")
        return {
            "statusCode": 200,
            "body": 'New product was added',
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