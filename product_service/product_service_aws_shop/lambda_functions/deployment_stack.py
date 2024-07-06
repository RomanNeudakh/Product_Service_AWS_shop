from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb_,
)
import boto3
from constructs import Construct
from .get_product_by_id import GetProductById
from .get_products_list import GetProductsList
from .apigateway_stack import ApiGatewayStack
from .create_table import CreateTable
from .create_product import CreateProduct
from .create_catalog_batch_process import CreateCatalogBatchProcess
class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        session = boto3.Session()
        region = session.region_name
        dynamodb = boto3.client('dynamodb', region_name=region)
        existing_tables = dynamodb.list_tables()['TableNames']
        create_product_stack = CreateProduct(self, 'CreateProductStackCrosscheck', 'Stock_Cross_Check_table', 'Product_Cross_Check_table', region)
        get_products_by_id_stack = GetProductById(self, 'GetProductByIdStackCrosscheck', 'Stock_Cross_Check_table', 'Product_Cross_Check_table', region)
        get_products_list_stack = GetProductsList(self, 'GetProductsListStackCrosscheck', 'Stock_Cross_Check_table', 'Product_Cross_Check_table', region)
        if 'Product_Cross_Check_table' not in existing_tables:
            CreateTable(self, 'CreateProductTable', 'Product_Cross_Check_table', 'id')
        if 'Stock_Cross_Check_table' not in existing_tables:
            CreateTable(self, 'CreateStockTable', 'Stock_Cross_Check_table', 'product_id')
        stock_table = dynamodb_.Table.from_table_name(self, 'StockTable', 'Stock_Cross_Check_table')
        stock_table.grant_read_write_data(get_products_by_id_stack.lambda_function)
        stock_table.grant_read_write_data(get_products_list_stack.lambda_function)
        stock_table.grant_read_write_data(create_product_stack.lambda_function)
        product_table = dynamodb_.Table.from_table_name(self, 'ProductTable', 'Product_Cross_Check_table')
        product_table.grant_read_write_data(get_products_by_id_stack.lambda_function)
        product_table.grant_read_write_data(get_products_list_stack.lambda_function)
        product_table.grant_read_write_data(create_product_stack.lambda_function)
        CreateCatalogBatchProcess(self, 'CreateCatalogBatchProcessCrosscheck', 'Stock_Cross_Check_table', 'Product_Cross_Check_table')
        ApiGatewayStack(
            self,
            'ApiGatewayStackCrosscheck',
            get_products_by_id_lambda=get_products_by_id_stack.lambda_function,
            get_products_list_lambda=get_products_list_stack.lambda_function,
            create_product_lambda=create_product_stack.lambda_function
        )