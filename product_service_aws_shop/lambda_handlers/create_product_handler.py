import json
import logging
import os
import uuid
import boto3

def createProductHandler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(f"Received event: {json.dumps(event)}")
    logger.info(f"Context: {context}")
    try:
        dynamodb = boto3.client('dynamodb', region_name=os.getenv('Region_name'))
        stock_table_name = os.getenv('Stock_table_name')
        product_table_name = os.getenv('Product_table_name')
        if not stock_table_name or not product_table_name:
            raise ValueError("Environment variables for table names are not set.")
        body = json.loads(event['body'])
        product_id = str(uuid.uuid4())
        title = body['title']
        description = body.get('description', '')
        price = body['price']
        count = body['count']
        product_item = {
            'id': {'S': product_id},
            'title': {'S': title},
            'description': {'S': description},
            'price': {'N': str(price)}
        }
        
        stock_item = {
            'product_id': {'S': product_id},
            'count': {'N': str(count)}
        }
        logger.info(f"Product was added: {product_item}")
        response = dynamodb.transact_write_items(
            TransactItems=[
                {
                    'Put': {
                        'TableName': product_table_name,
                        'Item': product_item
                    }
                },
                {
                    'Put': {
                        'TableName': stock_table_name,
                        'Item': stock_item
                    }
                }
            ]
        )
        logger.info(f"Transaction response: {response}")
        logger.info(f"Product created: {product_item}")
        return {
            "statusCode": 200,
            "body": f'New product was added: {product_item}',
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "POST",
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
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Origin": "*"
            }
        }