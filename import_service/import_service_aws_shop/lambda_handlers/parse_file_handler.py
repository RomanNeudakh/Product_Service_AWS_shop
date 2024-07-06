import json
import logging
import os
import boto3
import csv
from io import StringIO
logger = logging.getLogger()
logger.setLevel(logging.INFO)
s3_client = boto3.client('s3')
sqs = boto3.client('sqs')
def parseFileHandler(event, context):
    queue_name = os.getenv('QUEUE_NAME')
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    if not object_key.startswith('uploaded/'):
        logger.info(f"File {object_key} is not in the 'uploaded/' folder. Skipping.")
        return
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = s3_response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(file_content))
    for row in csv_reader:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(row)
        )
        logger.info(f"Parsed row: {json.dumps(row)}")
    new_object_key = object_key.replace('uploaded/', 'parsed/', 1)
    s3_client.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key},
        Key=new_object_key
    )
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    logger.info(f"File moved to {new_object_key}")