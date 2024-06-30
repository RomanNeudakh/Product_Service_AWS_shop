import json
import logging
import os
import boto3
class MissingQueryParameterError(Exception):
    pass
def importFileHandler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        s3_client = boto3.client('s3')
        bucket_name = os.getenv('BUCKET_NAME')
        file_name = event['queryStringParameters'].get('name')
        key = f"uploaded/{file_name}"
        logger.info(f"request to create a signed_url in bucket: {bucket_name} with key {key}")
        if not file_name:
            raise MissingQueryParameterError('Missing "name" query parameter')
        signed_url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=3600
        )
        logger.info(f"signed_url was created: {signed_url}")
        return {
            "statusCode": 200,
            "body": signed_url,
            "headers": {
                "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, OPTIONS",
                "Access-Control-Allow-Origin": "*"
            }
        }
    except MissingQueryParameterError as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
    }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal server error: {str(e)}"}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*"
            }
        }