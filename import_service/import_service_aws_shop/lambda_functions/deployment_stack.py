from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct
from .apigateway_stack import ApiGatewayStack
from .import_products import ImportProducts
from .parse_products import ParseProducts
class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        bucket_name="import-csv-bucket-task5"
        ParseProducts(self, 'ParseProductsStackCrosscheck', bucket_name)
        import_products_stack = ImportProducts(self, 'ImportProductsStackCrosscheck', bucket_name)
        ApiGatewayStack(
            self,
            'ApiGatewayStackCrosscheck',
            import_lambda=import_products_stack.lambda_function,
        )