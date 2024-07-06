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
            products_for_sns.append({
                'id': product_id,
                'title': title,
                'description': description,
                'price': price,
                'count': count
            })
        if products_for_sns:
            for product in products_for_sns:
                sns.publish(
                    TopicArn=sns_topic_arn,
                    Message=json.dumps(product),
                    MessageAttributes={
                        'title': {
                            'DataType': 'String',
                            'StringValue': product['title']
                        }
                    }
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