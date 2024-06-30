import json
import logging
import os
import boto3

def getProductsListHandler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(f"Received event: {json.dumps(event)}")
    logger.info(f"Context: {context}")
    try:
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('Region_name'))
        stock_table_name = os.getenv('Stock_table_name')
        product_table_name = os.getenv('Product_table_name')
        if not stock_table_name or not product_table_name:
            raise ValueError("Environment variables for table names are not set.")
        stock_table = dynamodb.Table(stock_table_name)
        response_stock = stock_table.scan()
        stocks = response_stock.get('Items', [])
        product_table = dynamodb.Table(product_table_name)
        response_products = product_table.scan()
        products = response_products.get('Items', [])
        for product in products:
            if 'price' in product:
                product['price'] = str(product['price'])
            for stock in stocks:
                if product['id'] == stock['product_id']:
                    product['count'] = str(stock['count'])
        return {
            "statusCode": 200,
            "body": json.dumps(products),
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
            "body": json.dumps({"message": "Internal server error"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Origin": "*"
            }
        }