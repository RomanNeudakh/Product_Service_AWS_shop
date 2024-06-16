from aws_cdk import (
    aws_lambda as lambda_,
    Stack,
)
from constructs import Construct

class GetProductsList(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.lambda_function = lambda_.Function(
            self,
            'GetProductsList',
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset('product_service_aws_shop/lambda_handlers/'),
            handler='get_products_list_handler.getProductsListHandler',
        )
