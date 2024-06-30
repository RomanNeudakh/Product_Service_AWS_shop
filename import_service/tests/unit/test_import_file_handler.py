import json
import sys
from pathlib import Path
from moto import mock_aws
sys.path.append(str(Path(__file__).parents[2]))
from import_service_aws_shop.lambda_handlers.import_file_handler import importFileHandler

@mock_aws
def test_import_file_handler_success():
    event = {
        "queryStringParameters": {
            "name": "test.csv"
        }
    }
    context = {}
    response = importFileHandler(event, context)
    assert "uploaded/test.csv" in response['body']
    assert response['statusCode'] == 200
    assert "https://" in response['body']
    assert response['headers']['Access-Control-Allow-Origin'] == "*"
    
@mock_aws
def test_import_file_handler_missing_name():
    event = {
        "queryStringParameters": {}
    }
    context = {}
    response = importFileHandler(event, context)
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['message'] == 'Missing "name" query parameter'
    assert response['headers']['Access-Control-Allow-Origin'] == "*"

@mock_aws
def test_import_file_handler_internal_error(mocker):
    mocker.patch('import_service_aws_shop.lambda_handlers.import_file_handler.boto3.client', side_effect=Exception("Some error"))
    event = {
        "queryStringParameters": {
            "name": "test.csv"
        }
    }
    context = {}
    response = importFileHandler(event, context)
    assert response['statusCode'] == 500
    body = json.loads(response['body'])
    assert "Internal server error" in body['message']
    assert response['headers']['Access-Control-Allow-Origin'] == "*"
