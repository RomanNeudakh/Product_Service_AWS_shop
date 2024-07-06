import os
import json
import uuid
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

def catalogBatchProcessHandler(event, context):
    try:
        product_table_name = os.environ['PRODUCT_TABLE']
        stock_table_name = os.environ['STOCK_TABLE']
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        products_for_sns = []
        if not stock_table_name or not product_table_name:
            raise ValueError("Environment variables for table names are not set.")
        for record in event['Records']:
            body = json.loads(record['body'])
            product_id = str(uuid.uuid4())
            title = body['title']
            description = body.get('description', '')
            price = body['price']
            count = body['count']
            if not title:
                logger.info(f"Skipping record due to invalid title: {body}")
                continue
            try:
                price = float(price)
                if price <= 0:
                    raise ValueError("Price must be greater than zero")
            except (ValueError, TypeError):
                logger.info(f"Skipping record due to invalid price: {body}")
                continue
            try:
                count = int(count)
                if count <= 0:
                    raise ValueError("Count must be a positive integer")
            except (ValueError, TypeError):
                logger.info(f"Skipping record due to invalid count: {body}")
                continue
            if not description:
                logger.info(f"Skipping record due to invalid count: {body}")
                continue
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
            dynamodb.transact_write_items(
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
            product_item['count'] = {'N': str(count)}
            products_for_sns.append(product_item)
        if products_for_sns:
            formatted_products = "\n\n".join(
                f"Product ID: {product['id']}\n"
                f"Title: {product['title']}\n"
                f"Description: {product['description']}\n"
                f"Price: {product['price']}\n"
                f"Count: {product['count']}"
                for product in products_for_sns
            )
            sns_report = f"Products from csv were added:\n\n{formatted_products}"
            sns.publish(
                TopicArn=os.getenv('SNS_TOPIC_ARN'),
                Message=sns_report
            )
        return {'statusCode': 200, 'body': 'Batch processed successfully'}
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