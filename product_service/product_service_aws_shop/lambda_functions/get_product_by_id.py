from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
)
from constructs import Construct

class GetProductById(Stack):
    def __init__(self, scope: Construct, construct_id: str, stock_table_name: str, product_table_name: str, region: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.lambda_function = lambda_.Function(
            self, 
            'GetProductsById',
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset('product_service_aws_shop/lambda_handlers/'),
            handler='get_product_by_id_handler.getProductByIdHandler',
            environment={
                'Stock_table_name': stock_table_name,
                'Product_table_name': product_table_name,
                'Region_name': region
            }
        )