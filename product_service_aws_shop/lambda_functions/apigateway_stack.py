from aws_cdk import (
    aws_apigateway as apigateway,
    Stack,
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, id: str, get_products_by_id_lambda, get_products_list_lambda, create_product_lambda, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        api = apigateway.RestApi(
            self, 
            "ProductServiceApi",
            rest_api_name="Product Service",
            description="This service serves products.",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"]
            )
        )

        create_product_integration = apigateway.LambdaIntegration(create_product_lambda)
        create_product_resource = api.root.add_resource("product")
        create_product_resource.add_method("POST", create_product_integration)

        get_products_list_integration = apigateway.LambdaIntegration(get_products_list_lambda)
        products_resource = api.root.add_resource("products")
        products_resource.add_method("GET", get_products_list_integration)

        get_products_by_id_integration = apigateway.LambdaIntegration(get_products_by_id_lambda)
        product_resource = products_resource.add_resource("{id}")
        product_resource.add_method("GET", get_products_by_id_integration)