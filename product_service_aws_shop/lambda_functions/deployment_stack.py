from aws_cdk import (
    Stack,
)
import boto3
from constructs import Construct
from .get_product_by_id import GetProductById
from .get_products_list import GetProductsList
from .apigateway_stack import ApiGatewayStack
from .create_table import CreateTable

class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        session = boto3.Session()
        region = session.region_name
        dynamodb = boto3.client('dynamodb', region_name=region)
        existing_tables = dynamodb.list_tables()['TableNames']
        if 'Product_Cross_Check_table' not in existing_tables:
            CreateTable(self, 'CreateProductTable', 'Product_Cross_Check_table', 'product_id')
        if 'Stock_Cross_Check_table' not in existing_tables:
            CreateTable(self, 'CreateStockTable', 'Stock_Cross_Check_table', 'id')
        
        get_products_by_id_stack = GetProductById(self, 'GetProductByIdStackCrosscheck')
        get_products_list_stack = GetProductsList(self, 'GetProductsListStackCrosscheck')
        ApiGatewayStack(
            self,
            'ApiGatewayStackCrosscheck',
            get_products_by_id_lambda=get_products_by_id_stack.lambda_function,
            get_products_list_lambda=get_products_list_stack.lambda_function
        )