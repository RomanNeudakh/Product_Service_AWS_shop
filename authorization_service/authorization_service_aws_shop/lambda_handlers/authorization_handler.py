import logging
import os
from base64 import b64decode

def generate_policy(principal_id, effect, resource):
    auth_response = {
        'principalId': principal_id
    }
    if effect and resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Action': 'execute-api:Invoke',
                    'Effect': effect,
                    'Resource': resource
                }
            ]
        }
        auth_response['policyDocument'] = policy_document
    return auth_response

def authorizationHandler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    try:
        username = ''
        token = event['authorizationToken']
        decoded_credentials = b64decode(token).decode('utf-8')
        username, password = decoded_credentials.split(':')
        expected_password = os.getenv(username)
        if not expected_password or expected_password != password:
            return generate_policy(username, 'Deny', event['methodArn'])
        return generate_policy(username, 'Allow', event['methodArn'])
    except Exception as e:
        logger.info(f"token decoding error: {e}")
        return generate_policy(username, 'Deny', event['methodArn'])