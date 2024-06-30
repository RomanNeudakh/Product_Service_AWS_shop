import json
import logging
import boto3
import csv
from io import StringIO

s3_client = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def parseFileHandler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    if not object_key.startswith('uploaded/'):
        logger.info(f"File {object_key} is not in the 'uploaded/' folder. Skipping.")
        return
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    file_content = s3_response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(StringIO(file_content))
    for row in csv_reader:
        logger.info(f"Parsed row: {json.dumps(row)}")
    new_object_key = object_key.replace('uploaded/', 'parsed/', 1)
    s3_client.copy_object(
        Bucket=bucket_name,
        CopySource={'Bucket': bucket_name, 'Key': object_key},
        Key=new_object_key
    )
    s3_client.delete_object(Bucket=bucket_name, Key=object_key)
    logger.info(f"File moved to {new_object_key}")