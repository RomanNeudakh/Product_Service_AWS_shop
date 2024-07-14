import json
import boto3
from moto import mock_aws
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))

from product_service_aws_shop.lambda_handlers.get_products_list_handler import getProductsListHandler



@mock_aws
def setup_products():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.create_table(
        TableName='Product_Cross_Check_table',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


    table.put_item(Item={'id': '1','description': 'test desc', 'title': 'product id 1', 'price': '100'})
    table.put_item(Item={'id': '2','description': 'test desc', 'title': 'product id 2', 'price': '110'})
    table.put_item(Item={'id': '3','description': 'test desc', 'title': 'product id 3', 'price': '120'})
    table.put_item(Item={'id': '4','description': 'test desc', 'title': 'product id 4', 'price': '130'})
    table.put_item(Item={'id': '5','description': 'test desc', 'title': 'product id 5', 'price': '140'})
    table.put_item(Item={'id': '6','description': 'test desc', 'title': 'product id 6', 'price': '150'})

    return table


@mock_aws
def setup_stock():
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.create_table(
        TableName='Stock_Cross_Check_table',
        KeySchema=[
            {
                'AttributeName': 'product_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
             {
                'AttributeName': 'product_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    table.put_item(Item={'product_id': '1', 'count': 100})
    table.put_item(Item={'product_id': '2', 'count': 110})
    table.put_item(Item={'product_id': '3', 'count': 120})
    table.put_item(Item={'product_id': '4', 'count': 130})
    table.put_item(Item={'product_id': '5', 'count': 140})
    table.put_item(Item={'product_id': '6', 'count': 150})

    return table

@mock_aws
def test_getProductsListHandler():
    setup_products()
    setup_stock()
    
    event = {}
    context = {}
    response = getProductsListHandler(event, context)
    
    assert response['statusCode'] == 200
    assert response['headers']['Content-Type'] == 'application/json'
    assert response['headers']['Access-Control-Allow-Methods'] == 'GET'
    assert response['headers']['Access-Control-Allow-Origin'] == '*'
    
    products = json.loads(response['body'])
    assert isinstance(products, list)
    assert len(products) == 6
    
    expected_products = [
        {'id': '1', 'description': 'test desc', 'title': 'product id 1', 'price': '100', 'count': '100'},
        {'id': '2', 'description': 'test desc', 'title': 'product id 2', 'price': '110', 'count': '110'},
        {'id': '3', 'description': 'test desc', 'title': 'product id 3', 'price': '120', 'count': '120'},
        {'id': '4', 'description': 'test desc', 'title': 'product id 4', 'price': '130', 'count': '130'},
        {'id': '5', 'description': 'test desc', 'title': 'product id 5', 'price': '140', 'count': '140'},
        {'id': '6', 'description': 'test desc', 'title': 'product id 6', 'price': '150', 'count': '150'},
    ]
    
    assert products == expected_products
