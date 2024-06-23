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
        request_model = api.add_model(
            "RequestModel",
            content_type="application/json",
            model_name="RequestModel",
            schema=apigateway.JsonSchema(
                schema=apigateway.JsonSchemaVersion.DRAFT4,
                title="Product",
                type=apigateway.JsonSchemaType.OBJECT,
                properties={
                    "count": apigateway.JsonSchema(type=apigateway.JsonSchemaType.NUMBER, minimum=0),
                    "price": apigateway.JsonSchema(type=apigateway.JsonSchemaType.NUMBER, minimum=1),
                    "description": apigateway.JsonSchema(type=apigateway.JsonSchemaType.STRING),
                    "title": apigateway.JsonSchema(type=apigateway.JsonSchemaType.STRING)
                },
                required=["count", "price", "description", "title"],
                additionalProperties=False
            )
        )
        request_validator = apigateway.RequestValidator(
            self, "RequestValidator",
            rest_api=api,
            request_validator_name="RequestValidator",
            validate_request_body=True,
            validate_request_parameters=False
        )

        create_product_integration = apigateway.LambdaIntegration(create_product_lambda)
        create_product_resource = api.root.add_resource("products")
        create_product_resource.add_method(
            "POST", 
            create_product_integration, 
            request_validator=request_validator,
            request_models={"application/json": request_model}
        )
        get_products_list_integration = apigateway.LambdaIntegration(get_products_list_lambda)
        create_product_resource.add_method("GET", get_products_list_integration)

        get_products_by_id_integration = apigateway.LambdaIntegration(get_products_by_id_lambda)
        product_resource = create_product_resource.add_resource("{id}")
        product_resource.add_method("GET", get_products_by_id_integration)