from aws_cdk import (
    Stack,
)
from constructs import Construct
from .get_product_by_id import GetProductById
from .get_products_list import GetProductsList
from .apigateway_stack import ApiGatewayStack

class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        get_products_by_id_stack = GetProductById(self, 'GetProductByIdStackCrosscheck')
        get_products_list_stack = GetProductsList(self, 'GetProductsListStackCrosscheck')
        ApiGatewayStack(
            self,
            'ApiGatewayStackCrosscheck',
            get_products_by_id_lambda=get_products_by_id_stack.lambda_function,
            get_products_list_lambda=get_products_list_stack.lambda_function
        )