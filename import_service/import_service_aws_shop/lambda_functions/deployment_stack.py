from aws_cdk import (
    Stack
)
from constructs import Construct
from .apigateway_stack import ApiGatewayStack
from .import_products import ImportProducts
from .parse_products import ParseProducts
class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        ParseProducts(self, 'ParseProductsStackCrosscheck')
        import_products_stack = ImportProducts(self, 'ImportProductsStackCrosscheck')
        ApiGatewayStack(
            self,
            'ApiGatewayStackCrosscheck',
            import_lambda=import_products_stack.lambda_function,
        )