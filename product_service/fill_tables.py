import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid4
from faker import Faker

fake = Faker()
session = boto3.Session()
region = session.region_name
dynamodb = boto3.resource('dynamodb', region_name=region)
products_table = dynamodb.Table('Product_Cross_Check_table')
stocks_table = dynamodb.Table('Stock_Cross_Check_table')
products = [
    {
        'id': str(uuid4()),
        'title': fake.word(),
        'description': fake.sentence(),
        'price': fake.random_int(min=10, max=100)
    }
    for _ in range(10)
]

stocks = [
    {
        'product_id': product['id'],
        'count': fake.random_int(min=1, max=50)
    }
    for product in products
]

with products_table.batch_writer() as batch:
    for product in products:
        batch.put_item(Item=product)

with stocks_table.batch_writer() as batch:
    for stock in stocks:
        batch.put_item(Item=stock)

print("Tables have been filled with test data.")